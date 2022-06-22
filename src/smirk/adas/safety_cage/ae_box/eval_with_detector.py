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
from pathlib import Path
from time import time

import numpy as np
import pandas as pd
import torch

import smirk.config.paths as paths
from smirk.adas.pedestrian_detector.yolo.val import results_by_slice


def eval_with_detector(
    ae_box_res_path: Path,
    conf_threshold: float,
    outlier_threshold: float,
    distance_threshold: float,
):
    save_dir = (
        paths.temp_dir_path / "ae_box" / f"{int(time())}_eval_pedestrian_detection"
    )
    save_dir.mkdir(parents=True)
    df: pd.DataFrame = pd.read_pickle(ae_box_res_path)

    ae_mask = (df.current_distance > distance_threshold) & (
        df.instance_score > outlier_threshold
    )
    df.loc[ae_mask, "img_res"] = df[ae_mask].apply(get_outlier_img_res, axis=1)
    df.loc[ae_mask, "predictions"] = df.loc[ae_mask, "predictions"].map(
        lambda _: np.array([])
    )

    results_by_slice(df, save_dir, conf_threshold)


def get_outlier_img_res(row):
    if not row.has_label:
        return None

    tcls = row.labels[:, 0].tolist()
    return (
        torch.zeros(0, 10, dtype=torch.bool),
        torch.Tensor(),
        torch.Tensor(),
        tcls,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        required=True,
        help="path to ae_box results pickle",
    )
    parser.add_argument(
        "--conf", required=True, type=float, help="confidence threshold"
    )
    parser.add_argument(
        "--outlier", required=True, type=float, help="outlier threshold"
    )
    parser.add_argument(
        "--distance", required=True, type=float, help="distance threshold"
    )
    args = parser.parse_args()

    eval_with_detector(args.data, args.conf, args.outlier, args.distance)
