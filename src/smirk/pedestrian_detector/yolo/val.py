"""
Custom yolov5 validation script adapted from ultralytics/yolov5 val.py

TODO: Extract a lot of this when adding next pedestrian model.
"""
import argparse
from pathlib import Path
from threading import Thread
from time import time
from typing import Dict, List, Optional, Tuple, cast

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm

import config.paths
from smirk.pedestrian_detector.yolo.metrics import (
    box_iou,
    calculate_base_metrics,
    draw_boxes,
)
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.datasets import create_dataloader
from yolov5.utils.general import (
    check_img_size,
    non_max_suppression,
    scale_coords,
    xywh2xyxy,
)
from yolov5.utils.plots import output_to_target, plot_images
from yolov5.utils.torch_utils import select_device

ImgRes = Tuple[
    torch.Tensor,  # [0] correct at iou level => Tensor[Predictions x iou_lvls(default=10)]
    torch.Tensor,  # [1] predicted conf => Tensor[Predictions]
    torch.Tensor,  # [2] predicted cls => Tensor[Predictions]
    List,  # [3] true cls => List[Labels]
]

FEMALE_PEDESTRIAN = {"female_casual", "female_business", "female_business_casual"}
MALE_PEDESTRIAN = {
    "male_casual",
    "male_business",
    "male_construction",
    "male_business_casual",
}
CHILD_PEDESTRIAN = {"child"}

PEDESTRIAN_OBJECTS = {*FEMALE_PEDESTRIAN, *MALE_PEDESTRIAN, *CHILD_PEDESTRIAN}
NON_PEDESTIAN_OBJECTS = {"box", "sphere", "pyramid", "cone", "cylinder"}


@torch.no_grad()
def evaluate(
    data: str,
    weights: str,
    batch_size: int = 256,
    img_size: int = 640,
    iou_thres: float = 0.6,
) -> None:
    """Evaluate model on dataset

    Args:
        data_dir: Dataset dir path
        weights: Path to model.pt
        batch_size: Batch size
        img_size: Inference size (pixels)
        iou_thres: Non-max supression IoU threshold
    """
    device = select_device(batch_size=batch_size)  # cuda | cpu

    save_dir = config.paths.temp_dir_path / "yolo" / "eval" / str(int(time()))
    save_dir.mkdir(parents=True)

    model = DetectMultiBackend(weights, device)
    model.model.float()

    model.eval()
    img_size = check_img_size(img_size, s=model.stride)  # type:ignore
    model.warmup(imgsz=(1, 3, img_size, img_size))

    metadata = pd.read_csv(Path(data) / "metadata.csv")

    dataloader = create_dataloader(
        data,
        img_size,
        batch_size,
        model.stride,
        single_cls=False,
        pad=0.5,
        rect=True,
    )[0]

    # Configure
    iouv = torch.linspace(0.5, 0.95, 10).to(device)  # iou vector 0.5:0.95

    seen = 0
    stats: List[ImgRes] = []
    augmented_res = {}

    for batch_i, (im, targets, paths, shapes) in enumerate(tqdm(dataloader)):

        # Preprocess
        im = im.to(device, non_blocking=True)
        im = im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        *_, height, width = im.shape  # batch size, channels, height, width

        # [Total targetx x 6] = Tensor[[img_index, class, ...xcycwh-rel]]
        targets = targets.to(device)

        # Inference
        out, _ = model(im, val=True)  # inference, loss outputs

        # NMS

        # Out format (after NMS), sligthly unclear before NMS...
        # [Images x Predictions x [...xyxy-abs, conf, class]]
        # List[Tensor[Tensor[]]]
        # Looks like bboxes are in xyxy-abs format
        out = non_max_suppression(prediction=out, conf_thres=0.001, iou_thres=iou_thres)

        targets[:, 2:] *= torch.Tensor([width, height, width, height]).to(
            device
        )  # to pixels i.e. Tensor[img_index, class, ...xcycwh-abs]

        # Metrics
        # Pred: Tensor[Predictions x [...xyxy-abs, conf class]]
        for si, pred in enumerate(out):  # for each image
            seen += 1
            path = Path(paths[si])  # path to img,
            shape = shapes[si][0]  # original img dimensions

            # Labels: Each target where image_index matches current index excluding image_index col
            #         i.e. all targets in current image [Targets x [class, ...xcyxcwh-abs]]
            labels = targets[targets[:, 0] == si, 1:]
            # target class, one entry for each labeled object

            labelsn = torch.Tensor()
            if len(labels):
                tbox = xywh2xyxy(labels[:, 1:5])  # target boxes [xyxy-abs]
                scale_coords(
                    im[si].shape[1:], tbox, shape, shapes[si][1]
                )  # native-space labels
                labelsn = torch.cat((labels[:, 0:1], tbox), 1)  # native-space labels

            predn = pred.clone()
            if len(pred):
                # Predictions
                # native-space pred
                # bbox was predicted on rescaled image (i.e. multiple of 32)
                # now we scale the predicted bbox to match the orignal image shape
                scale_coords(im[si].shape[1:], predn[:, :4], shape, shapes[si][1])

            img_res = evaluate_single_img(labelsn, predn, iouv)

            if img_res is not None:
                stats.append(img_res)

            append_augmented_img_res(
                augmented_res, path, metadata, labelsn, predn, img_res
            )

        # Plot prediction examples
        if batch_i < 3:
            plot_batch_predictions(batch_i, save_dir, im, targets, out, paths)

    augmented_res_df = pd.DataFrame.from_dict(augmented_res, orient="index")
    augmented_res_df.sort_values(by=["run_id", "frame_index"], inplace=True)
    augmented_res_df.reset_index(inplace=True, drop=True)
    augmented_res_df.to_pickle(save_dir / f"{Path(data).stem}-augmented-res.pkl")

    results_by_slice(augmented_res_df, save_dir)


def evaluate_single_img(
    labels: torch.Tensor, pred: torch.Tensor, iouv: torch.Tensor
) -> Optional[ImgRes]:
    """Evaluate single image

    Args:
        labels: Image labels [class, ...xyxyA][]
        preds: Image predictions [...xyxyA, conf, class][]
        iouv: IoU vector
    """
    has_labels = len(labels) > 0
    has_preds = len(pred) > 0
    tcls = labels[:, 0].tolist() if has_labels else []
    niou = iouv.numel()

    if not has_preds:
        if has_labels:
            return (
                torch.zeros(0, niou, dtype=torch.bool),
                torch.Tensor(),
                torch.Tensor(),
                tcls,
            )

        return None

    if has_labels:
        correct = create_iou_table(pred, labels, iouv)
    else:
        correct = torch.zeros(pred.shape[0], niou, dtype=torch.bool)

    return (
        correct.cpu(),  # Correct
        pred[:, 4].cpu(),  # Conf
        pred[:, 5].cpu(),  # Predicted class
        tcls,  # True class
    )


def create_iou_table(
    detections: torch.Tensor, labels: torch.Tensor, iouv: torch.Tensor
) -> torch.Tensor:
    """Calculates for what iou-level each detections is correct.

    Args:
        detections: Tensor[L, [...xyxy-abs, conf, class]]
        labels: Tensor[M, [class, ...xyxy-abs]]
        iouv: IoU vector Tensor[N]

    Returns:
        A matrix (Tensor[L, N]) indicating at what iou-level each deteciton is correct.
    """
    correct = torch.zeros(
        detections.shape[0], iouv.shape[0], dtype=torch.bool, device=iouv.device
    )
    iou = box_iou(labels[:, 1:], detections[:, :4])  # [Labels x Detections]

    # IoU above threshold=0.5 and classes match
    # equivalent to torch.nonzero with as_tuple=True
    # will be tuple[Tensor[index in lables], Tensor[index in detections]]
    # were condition is met.
    x = torch.where((iou >= iouv[0]) & (labels[:, 0:1] == detections[:, 5]))

    if x[0].shape[0]:  # if there are any matches at iou=0.5
        matches = (
            torch.cat((torch.stack(x, 1), iou[x[0], x[1]][:, None]), 1).cpu().numpy()
        )  # [label, detection, iou]

        if x[0].shape[0] > 1:
            matches = matches[matches[:, 2].argsort()[::-1]]  # sort by iou
            matches = matches[
                np.unique(matches[:, 1], return_index=True)[1]
            ]  # If detection matches multiple labels use highest iou match
            matches = matches[
                np.unique(matches[:, 0], return_index=True)[1]
            ]  # If label is matched by multiple detections use the one with hightes iou
        matches = torch.Tensor(matches).to(iouv.device)
        correct[matches[:, 1].long()] = (
            matches[:, 2:3] >= iouv
        )  # for each match, check if it fulfills iou thres 0.5:0.95

    return correct  # iou table for all detections


def plot_batch_predictions(batch_i, save_dir, im, targets, out, paths) -> None:
    """Saves predictions and groud truth images to disk."""
    names = {0: "pedestrian"}  # TODO: Assuming only pedestrians

    f = save_dir / f"val_batch{batch_i}_labels.jpg"
    Thread(target=plot_images, args=(im, targets, paths, f, names), daemon=True).start()

    f = save_dir / f"val_batch{batch_i}_pred.jpg"
    Thread(
        target=plot_images,
        args=(im, output_to_target(out), paths, f, names),
        daemon=True,
    ).start()


def append_augmented_img_res(
    results: Dict,
    img_path: Path,
    metadata: pd.DataFrame,
    labelsn: torch.Tensor,
    predn: torch.Tensor,
    img_res: Optional[ImgRes],
) -> None:
    frame_index = int(img_path.stem.replace("cam", ""))
    run_id = img_path.parent.stem
    res_id = f"{run_id}-{frame_index}"

    img_metadata = metadata[
        (metadata.run_id == run_id) & (metadata.frame_index == frame_index)
    ]

    if len(img_metadata) != 1:
        raise Exception(f"Invalid metadata for {res_id}, found {len(img_metadata)}")

    img_metadata = img_metadata.iloc[0][
        [
            "class_text",
            "object_type",
            "is_occluded",
            "current_distance",
            "start_distance_from_car",
            "angle",
            "speed",
            "scenario_type",
        ]
    ]

    results[res_id] = dict(
        run_id=run_id,
        frame_index=frame_index,
        img_path=img_path,
        labels=labelsn,
        predictions=predn,
        img_res=img_res,
        **dict(img_metadata),
    )


def evaluate_slice(slice, save_dir, conf_threshold) -> pd.DataFrame:
    save_dir.mkdir(exist_ok=True)
    total_imgs = len(slice)
    total_pedestrian = slice.class_text.value_counts().get("pedestrian", 0)

    slice_res = [np.concatenate(x, 0) for x in zip(*slice.img_res.dropna())]
    tp, fp, fn, p, r, f1, ap, conf = calculate_base_metrics(
        *slice_res,
        total_imgs=total_imgs,
        save_dir=save_dir,
        conf_threshold=conf_threshold,
    )
    ap50, ap = ap[:, 0], ap.mean(1)  # AP@0.5, AP@0.5:0.95

    res_df = pd.DataFrame(
        [
            [
                tp.sum(),
                fp.sum(),
                fn.sum(),
                p.mean(),
                r.mean(),
                fp.sum() / total_imgs,
                f1.mean(),
                ap50.mean(),
                ap.mean(),
                conf,
                total_imgs,
                total_pedestrian,
                (total_imgs - total_pedestrian),
            ]
        ],
        columns=[
            "True Positive",
            "False Positive",
            "False Negative",
            "Precision",
            "Recall",
            "FPPI",
            "F1",
            "AP@0.5",
            "AP@0.5:0.95",
            "Confidence threshold",
            "Total images",
            "Total pedestrian images",
            "Total non-pedestrian images",
        ],
    )

    res_df.to_csv(save_dir / "res.csv", index=False)

    return res_df


def results_by_slice(
    df: pd.DataFrame, save_dir: Path, conf_threshold: float = None
) -> None:
    all_res = evaluate_slice(df, save_dir / "all", conf_threshold=conf_threshold)
    conf_threshold = all_res["Confidence threshold"][0]

    df["fp"] = df.img_res.apply(is_fp, conf_threshold=conf_threshold)
    df["fn"] = df.img_res.apply(is_fn, conf_threshold=conf_threshold)

    slice_pedestrians = df[df.object_type.isin(PEDESTRIAN_OBJECTS)]

    # Pedestrians close to ego car
    slice_close_to_car_res = evaluate_slice(
        slice_pedestrians[slice_pedestrians.current_distance < 50],
        save_dir / "close_to_car",
        conf_threshold=conf_threshold,
    )

    # Pedestrians far from ego car
    slice_far_from_car_res = evaluate_slice(
        slice_pedestrians[slice_pedestrians.current_distance.between(50, 80)],
        save_dir / "far_from_car",
        conf_threshold=conf_threshold,
    )

    # Running pedestrians (speed >= 3 m/s) (SYS-ROB-REQ2)
    slice_running_res = evaluate_slice(
        slice_pedestrians[slice_pedestrians.speed >= 3],
        save_dir / "running",
        conf_threshold=conf_threshold,
    )

    # Walking pedestrians (speed > 0 m/s but < 3 m/s) (SYS-ROB-REQ2)
    slice_walking_res = evaluate_slice(
        slice_pedestrians[slice_pedestrians.speed.between(1, 2)],
        save_dir / "walking",
        conf_threshold=conf_threshold,
    )

    # Occluded pedestrians (entering or leaving the field of view) (DAT-COM-REQ4)
    slice_occluded_res = evaluate_slice(
        slice_pedestrians[slice_pedestrians.is_occluded],
        save_dir / "occluded",
        conf_threshold=conf_threshold,
    )

    # Male pedestrians (DAT-COM-REQ2)
    slice_male = df[df.object_type.isin(MALE_PEDESTRIAN)]
    slice_male_res = None
    if len(slice_male):
        slice_male_res = evaluate_slice(
            slice_male, save_dir / "male", conf_threshold=conf_threshold
        )

    # Female pedestrians (DAT-COM-REQ2)
    slice_female = df[df.object_type.isin(FEMALE_PEDESTRIAN)]
    slice_female_res = None
    if len(slice_female):
        slice_female_res = evaluate_slice(
            slice_female, save_dir / "female", conf_threshold=conf_threshold
        )

    # Children (DAT-COM-REQ2)
    slice_child = df[df.object_type.isin(CHILD_PEDESTRIAN)]
    slice_child_res = None
    if len(slice_child):
        slice_child_res = evaluate_slice(
            slice_child, save_dir / "child", conf_threshold=conf_threshold
        )

    # Distance <= 50m SYS-PER-REQ2
    slice_50 = df[df.current_distance <= 50]
    slice_50_res = evaluate_slice(
        slice_50, save_dir / "slice_50", conf_threshold=conf_threshold
    )

    # Distance <= 80m SYS-PER-REQ1, SYS-PER-REQ3, SYS-PER-REQ4
    slice_80 = df[df.current_distance <= 80]
    slice_80_res = evaluate_slice(
        slice_80, save_dir / "slice_80", conf_threshold=conf_threshold
    )

    all_slices_res = {
        "All": all_res,
        "Male": slice_male_res,
        "Female": slice_female_res,
        "Child": slice_child_res,
        "Close": slice_close_to_car_res,
        "Far": slice_far_from_car_res,
        "Running": slice_running_res,
        "Walking": slice_walking_res,
        "Occluded": slice_occluded_res,
        "<= 50": slice_50_res,
        "<= 80": slice_80_res,
    }

    all_slices_res = {
        name: res for name, res in all_slices_res.items() if res is not None
    }

    summary = cast(
        pd.DataFrame, pd.concat(list(all_slices_res.values()), ignore_index=True)
    )
    summary["FPPI"] = summary["False Positive"] / summary["Total images"]
    summary.insert(0, "Slice", all_slices_res.keys())  # type:ignore
    save_result_df(summary, save_dir, "all_slices_res")

    # Missed in 5 frame fram window at <=80
    rolling_sum_80 = (
        slice_80.groupby("run_id").fn.rolling(window=5, min_periods=5).sum()
    )
    rolling_sum_80_res = (
        rolling_sum_80.value_counts()
        .sort_index()
        .reset_index(drop=True)
        .rename_axis("missed in windows")
        .rename("occurences")
        .to_frame()
    )
    save_result_df(rolling_sum_80_res, save_dir, "rolling_80")

    # False positives by object type
    df_fp = df[df.fp]
    fp_count_res = (
        df_fp.object_type.value_counts()
        .rename_axis("Object type")
        .rename("False positives")
        .to_frame()
    )
    save_result_df(fp_count_res, save_dir, "fp_count_res")

    # Annotate false positive frames
    # TODO: Thread and extract
    fp_dir = save_dir / "fps"
    fp_dir.mkdir(exist_ok=True)
    for i, row in enumerate(df_fp.itertuples(index=True)):
        predictions_above_thresh = row.predictions[
            row.predictions[:, -2] > conf_threshold
        ]
        img_with_boxes = draw_boxes(row.img_path, row.labels, predictions_above_thresh)
        file_name = f"{row.Index}-{i:06}.jpg"
        img_with_boxes.save(fp_dir / file_name)

    # False negatives by object type
    df_fn = df[df.fn]
    fn_count_res = (
        df_fn.object_type.value_counts()
        .rename_axis("Object type")
        .rename("False negatives")
        .to_frame()
    )
    save_result_df(fn_count_res, save_dir, "fn_count_res")

    # Annotate false negative frames
    # TODO: Thread and extract
    fn_dir = save_dir / "fns"
    fn_dir.mkdir(exist_ok=True)
    for i, row in enumerate(df_fn.itertuples()):
        predictions_above_thresh = row.predictions[
            row.predictions[:, -2] > conf_threshold
        ]
        img_with_boxes = draw_boxes(row.img_path, row.labels, predictions_above_thresh)
        file_name = f"{row.Index}-{i:06}.jpg"
        img_with_boxes.save(fn_dir / file_name)

    # Maximum consecutive misses
    df["fn_sequence_length"] = df.groupby("run_id").fn.apply(
        lambda x: x * (x.groupby((x != x.shift()).cumsum()).cumcount() + 1)
    )
    consecutive_misses = (
        df.groupby("run_id")
        .fn_sequence_length.max()
        .sort_values()
        .rename("Maximum consecutive misses")
        .to_frame()
    )
    save_result_df(consecutive_misses, save_dir, "consecutive")


def save_result_df(df: pd.DataFrame, dir_path: Path, name: str) -> None:
    file_path = dir_path / f"{name}"
    file_path.with_suffix(".tex").write_text(df.to_latex(index=False))
    df.to_csv(file_path.with_suffix(".csv"), index=False)


def is_fp(img_res: ImgRes, conf_threshold: float) -> bool:
    if img_res is None:
        return False

    # TODO: Multiple FPs?
    return (~img_res[0][img_res[1] >= conf_threshold][:, 0]).sum().item() > 0


def is_fn(img_res: ImgRes, conf_threshold: float) -> bool:
    if img_res is None:
        return False

    tp = img_res[0][img_res[1] >= conf_threshold][:, 0].sum().item()
    label_count = len(img_res[3])

    # NOTE: Assuming at most 1 label/tp.
    assert tp < 2, "More than 1 tp"
    assert label_count < 2, "More than 1 label"

    return tp < label_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        required=True,
        help="path to dataset directory",
    )
    parser.add_argument(
        "--weights",
        default=str(config.paths.yolo_model),
        help="path to model weights",
    )

    args = parser.parse_args()

    evaluate(args.data, args.weights)
