#
# SMIRK
# Copyright (C) 2021-2022 RISE Research Institutes of Sweden AB
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Custom eval calculations and plots adapted from yolov5.utils.metrics

NOTE: Not tested for multiple classes.

TODO: Extract a lot of this when adding next pedestrian model.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch
from PIL import Image

from yolov5.utils.plots import Annotator

sns.set_theme(context="paper", palette="colorblind")


def find_conf_index(
    r: np.ndarray,
    p: np.ndarray,
    nt: np.ndarray,
    total_imgs: int,
    fppi_threshold=0.0001,
    eps=1e-16,
):
    """Find the maximum confidence index that keeps FPPI below the specified level.

    Args:
        r:  Recal
        conf:  Objectness value from 0-1 (nparray).
        pred_cls:  Predicted object classes (nparray).
        target_cls:  True object classes (nparray).
        save_dir:  Plot save directory

    TODO: Does this make sense for multiple classes?
    """
    tp = (r * nt).round()  # true positives / per confidence level
    fp = (tp / (p + eps) - tp).round()  # false positives / per confidence level
    fppi = fp / total_imgs

    return np.argmax(fppi < fppi_threshold, axis=1).max()


def calculate_base_metrics(
    tp,
    conf,
    pred_cls,
    target_cls,
    total_imgs: int,
    save_dir: Path,
    conf_threshold: float = None,
    eps=1e-16,
):
    """
    Args:
        tp:  True positives (nparray, nx1 or nx10).
        conf:  Objectness value from 0-1 (nparray).
        pred_cls:  Predicted object classes (nparray).
        target_cls:  True object classes (nparray).
        save_dir:  Plot save directory
    """
    # Sort by objectness
    i = np.argsort(-conf)
    tp, conf, pred_cls = tp[i], conf[i], pred_cls[i]

    # Find unique classes
    unique_classes, nt = np.unique(target_cls, return_counts=True)
    nc = unique_classes.shape[0]  # number of classes

    # Create Precision-Recall curve and compute AP for each class
    px, py = np.linspace(0, 1, 1001), []  # for plotting
    ap, p, r = np.zeros((nc, tp.shape[1])), np.zeros((nc, 1001)), np.zeros((nc, 1001))
    for ci, c in enumerate(unique_classes):
        i = pred_cls == c
        n_l = nt[ci]  # number of labels
        n_p = i.sum()  # number of predictions

        if n_p == 0 or n_l == 0:
            continue
        else:
            # Accumulate FPs and TPs
            fpc = (1 - tp[i]).cumsum(0)
            tpc = tp[i].cumsum(0)

            # Recall
            recall = tpc / (n_l + eps)  # recall curve
            r[ci] = np.interp(
                -px, -conf[i], recall[:, 0], left=0
            )  # negative x, xp because xp decreases

            # Precision
            precision = tpc / (tpc + fpc)  # precision curve
            p[ci] = np.interp(-px, -conf[i], precision[:, 0], left=1)  # p at pr_score

            # AP from recall-precision curve
            for j in range(tp.shape[1]):
                ap[ci, j], mpre, mrec = compute_ap(recall[:, j], precision[:, j])
                if j == 0:
                    py.append(np.interp(px, mrec, mpre))  # precision at mAP@0.5

    f1 = 2 * p * r / (p + r + eps)

    if conf_threshold is None:
        conf_index = find_conf_index(r, p, nt, total_imgs)
    else:
        conf_index = int(round(conf_threshold * 1000))

    plot_precision_recall(px, py, ap, save_dir / "PR_curve.png")
    plot_metric_confidence(px, f1, conf_index, save_dir / "F1_curve.png", ylabel="F1")
    plot_metric_confidence(
        px, p, conf_index, save_dir / "P_curve.png", ylabel="Precision"
    )
    plot_metric_confidence(px, r, conf_index, save_dir / "R_curve.png", ylabel="Recall")

    i = conf_index
    conf_threshold = (1 / 1000) * conf_index
    p = p[:, i]
    r = r[:, i]
    f1 = f1[:, i]
    tp = (r * nt).round()  # true positives
    fn = ((1 - r) * nt).round()
    fp = (tp / (p + eps) - tp).round()  # false positives

    return tp, fp, fn, p, r, f1, ap, conf_threshold


def compute_ap(recall, precision):
    """Compute the average precision, given the recall and precision curves
    # Arguments
        recall:    The recall curve (list)
        precision: The precision curve (list)
    # Returns
        Average precision, precision curve, recall curve
    """

    # Append sentinel values to beginning and end
    mrec = np.concatenate(([0.0], recall, [1.0]))
    mpre = np.concatenate(([1.0], precision, [0.0]))

    # Compute the precision envelope
    mpre = np.flip(np.maximum.accumulate(np.flip(mpre)))

    # Integrate area under curve
    method = "interp"  # methods: 'continuous', 'interp'
    if method == "interp":
        x = np.linspace(0, 1, 101)  # 101-point interp (COCO)
        ap = np.trapz(np.interp(x, mrec, mpre), x)  # integrate
    else:  # 'continuous'
        i = np.where(mrec[1:] != mrec[:-1])[0]  # points where x axis (recall) changes
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])  # area under curve

    return ap, mpre, mrec


# Plots ----------------------------------------------------------------------------------------------------------------
LABEL_FONTSIZE = 36
TICK_FONTSIZE = 28
LEGEND_FONTSIZE = 34


def plot_metric_confidence(px, py, conf, save_dir: Path, ylabel: str):
    y = py.mean(0)

    _, ax = plt.subplots(1, 1, figsize=(15, 15), tight_layout=True)
    ax.set_xlim([0, 1.01])
    ax.set_ylim([0, 1.01])
    ax.grid(True, linewidth=1)

    plt.ylabel(ylabel, fontsize=LABEL_FONTSIZE)
    plt.xlabel("Confidence", fontsize=LABEL_FONTSIZE)
    plt.xticks(fontsize=TICK_FONTSIZE)
    plt.yticks(fontsize=TICK_FONTSIZE)

    p = sns.lineplot(
        x=px,
        y=y,
        ax=ax,
        ci=None,
        label=f"{ylabel} {y[conf]:.3f} at confidence threshold {px[conf]:.3f}",
    )

    p.axvline(
        x=px[conf],
        color=sns.color_palette()[1],
        linestyle="--",
        label="Confidence threshold",
    )

    ax.legend(loc="lower left", fontsize=LEGEND_FONTSIZE)

    plt.savefig(save_dir)
    plt.close()


def plot_precision_recall(px, py, ap, save_dir: Path):
    py = np.stack(py, axis=1)

    plt.figure(figsize=(15, 15))
    plt.xlim([0, 1.01])
    plt.ylim([0, 1.01])
    plt.grid(True, linewidth=1)

    plt.xlabel("Recall", fontsize=LABEL_FONTSIZE)
    plt.ylabel("Precision", fontsize=LABEL_FONTSIZE)
    plt.xticks(fontsize=TICK_FONTSIZE)
    plt.yticks(fontsize=TICK_FONTSIZE)

    sns.lineplot(
        x=px,
        y=py.mean(1),
        drawstyle="steps-post",
        label=f"AP@50={ap[:, 0].mean():.3f}",
        ci=None,
    )

    plt.legend(loc="lower left", fontsize=LEGEND_FONTSIZE)
    plt.tight_layout()

    plt.savefig(save_dir, dpi=205)
    plt.close()


def draw_boxes(img_path: Path, labels: torch.Tensor, predictions: torch.Tensor):
    colors = np.array(sns.color_palette()) * 255
    annotator = Annotator(im=np.array(Image.open(img_path)), line_width=1)

    if len(labels):
        # NOTE:Assumung 1 label right now
        assert len(labels) == 1, "Found multiple labels"

        annotator.box_label(labels[0][1:5], label="label", color=colors[0])

    if len(predictions):
        annotator.box_label(predictions[0][0:4], label="prediction", color=colors[1])

    return Image.fromarray(annotator.result())


def box_iou(box1, box2):
    # https://github.com/pytorch/vision/blob/master/torchvision/ops/boxes.py
    """
    Return intersection-over-union (Jaccard index) of boxes.
    Both sets of boxes are expected to be in (x1, y1, x2, y2) format.
    Arguments:
        box1 (Tensor[N, 4])
        box2 (Tensor[M, 4])
    Returns:
        iou (Tensor[N, M]): the NxM matrix containing the pairwise
            IoU values for every element in boxes1 and boxes2
    """

    def box_area(box):
        # box = 4xn
        return (box[2] - box[0]) * (box[3] - box[1])

    area1 = box_area(box1.T)
    area2 = box_area(box2.T)

    # inter(N,M) = (rb(N,M,2) - lt(N,M,2)).clamp(0).prod(2)
    inter = (
        (
            torch.min(box1[:, None, 2:], box2[:, 2:])
            - torch.max(box1[:, None, :2], box2[:, :2])
        )
        .clamp(0)
        .prod(2)
    )
    return inter / (
        area1[:, None] + area2 - inter
    )  # iou = inter / (area1 + area2 - inter)


def fitness(x):
    w = [0.0, 0.0, 1, 0]  # weights for [P, R, mAP@0.5, mAP@0.5:0.95]
    return (x[:, :4] * w).sum(1)
