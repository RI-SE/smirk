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
import argparse
import concurrent.futures
from pathlib import Path
from time import time
from typing import cast

import numpy as np
import pandas as pd
import seaborn as sns
import torch  # noqa
from alibi_detect.od.ae import OutlierAE
from alibi_detect.utils.saving import load_detector
from PIL import Image
from tqdm import tqdm

import config.paths
from yolov5.utils.augmentations import letterbox


def evaluate_outlier(
    pedestrian_results_path: str,
    model_path: str,
    batch_size=1000,
) -> None:
    save_dir = config.paths.temp_dir_path / "ae_box" / f"{int(time())}_eval_outlier"
    save_dir.mkdir(parents=True)
    model = cast(OutlierAE, load_detector(model_path))

    df: pd.DataFrame = pd.read_pickle(pedestrian_results_path)

    df["has_pred"] = df.predictions.str.len() > 0
    df["has_label"] = df.labels.str.len() > 0

    chunks = np.array_split(df, len(df) // batch_size)
    for chunk in tqdm(chunks):
        with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            boxes = list(executor.map(extract_box, chunk[chunk.has_pred].itertuples()))

        chunk_res = model.predict(np.stack(boxes, 0), return_feature_score=False)
        chunk.loc[chunk.has_pred, "instance_score"] = chunk_res["data"]["instance_score"]  # type: ignore

    df = cast(pd.DataFrame, pd.concat(chunks, ignore_index=True))
    df.to_pickle(save_dir / "ae-box-aug-res.pkl")

    outlier_threshold = estimate_threshold(df)

    df.boxplot(column="instance_score", by="object_type").figure.savefig("box.png")

    df["object_color"] = color_series(df.object_type)

    for distance in range(0, 40, 10):
        plot_with_distance_threshold(
            df,
            distance,
            outlier_threshold,
            save_dir / f"scatter_{distance}.png",
        )
        df[
            (df.current_distance >= distance) & (df.instance_score > outlier_threshold)
        ].object_type.value_counts().to_csv(f"filtered_objects_{distance}.csv")


def extract_box(row):
    pred = row.predictions[0].cpu().numpy()
    im_box = np.array(Image.open(row.img_path).crop(pred[:4]))
    im_box_letter, *_ = letterbox(im_box, (160, 64), auto=False, scaleFill=True)

    return (im_box_letter / 255).astype(np.float32)


def estimate_threshold(df: pd.DataFrame):
    fraction_outliers = len(df[df.class_text == "object"]) / len(df)
    return df.instance_score.quantile(1 - fraction_outliers)


def plot_with_distance_threshold(
    df: pd.DataFrame,
    distance: float,
    threshold: float,
    save_path: Path,
):
    # TODO: Labels etc.
    ax = (
        df[df.current_distance > distance]
        .sort_values(by=["object_type", "current_distance"])  # type: ignore
        .reset_index(drop=True)
        .reset_index()
        .plot.scatter(x="index", y="instance_score", c="object_color", alpha=0.5)
    )
    ax.axhline(threshold, c="r", ls="--")
    ax.figure.savefig(save_path)


def color_series(s: pd.Series):
    unique = s.unique()
    colors = sns.color_palette("hls", len(unique)).as_hex()  # type: ignore
    cmap = dict(zip(unique, colors))

    return s.map(cmap)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        required=True,
        help="path to pedestrian_detector results pickle",
    )
    parser.add_argument(
        "--weights",
        default=str(config.paths.ae_box_model),
        help="path to model",
    )

    args = parser.parse_args()

    evaluate_outlier(args.data, args.weights)
