#
# SMIRK
# Copyright (C) 2021-2023 RISE Research Institutes of Sweden AB
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
import concurrent.futures
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Set, Tuple

import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm

from smirk.adas.safety_cage.ae_box.data import resize_box_img


@dataclass
class SplitResult:
    """Stores run ids for a train/val split."""

    train_ids: Set[str]
    val_ids: Set[str]


def split(label_paths: List[Path], val_size: float, seed: int) -> SplitResult:
    """Splits a dataset on smirk format into a train and val set.

    Object and scenario type is taken into when performing the split.

    Args:
        label_paths: Paths to labels on smirk format.
        val_size: Fraction of data to use for validation.
        seed: Random seed to use for splitting.

    Returns:
        SplitResult with run ids for the train and val datsets.
    """
    labels = pd.concat(
        [pd.read_csv(path) for path in label_paths],
        ignore_index=True,
    )

    grouped_scenario_ids = labels.groupby(
        ["object_type", "scenario_type"]
    ).run_id.unique()

    val_ids = set()
    for ids in grouped_scenario_ids:
        val_ids.update(pd.Series(ids).sample(frac=val_size, random_state=seed))

    train_ids = set(labels.run_id.unique()) - val_ids

    return SplitResult(train_ids, val_ids)


def _load_labels_with_abs_path(label_paths: List[Path]):
    labels_list = []

    for label_path in label_paths:
        df = pd.read_csv(label_path)
        label_dir = label_path.parent.resolve()
        df["abs_file_path"] = df.file.apply(lambda f: label_dir / f)
        labels_list.append(df)

    return pd.concat(labels_list, ignore_index=True)


def to_yolo(label_paths: List[Path], out_dir: Path, included_ids: pd.Series = None):
    """Converts a dataset on smirk format to yolo format.

    Images are symlinked so don't take up additional space. Deleting or moving the original images will break the symlinks.

    Args:
        label_paths: Paths to labels on smirk format.
        out_dir: Path to location for the yolo dataset.
        include_ids: Only include ids in the Series.
    """

    labels = _load_labels_with_abs_path(label_paths)

    if included_ids is not None:
        labels = labels[labels.run_id.isin(included_ids)]

    out_dir = out_dir.resolve()

    def process_dataset_row(row):
        new_img_path = out_dir / row.object_type / row.file
        label_path = new_img_path.with_suffix(".txt")
        new_img_path.parent.mkdir(parents=True, exist_ok=True)

        # Pathlib and os symlinks require "sudo" on windows (depending on system config?).
        # Using mklink directly works without sudo but is 10 times slower...
        # Possibly fallback on mklink if this fails.
        # subprocess.call(['mklink', str(new_img_path.absolute()), str(row.abs_file_path)], shell=True, stdout=subprocess.DEVNULL)
        new_img_path.symlink_to(row.abs_file_path)

        if row.class_text != "pedestrian":
            label_path.touch(exist_ok=True)
            return

        class_label = 0
        x_center = ((row.x_min + row.x_max) / 2) / row.image_width
        y_center = ((row.y_min + row.y_max) / 2) / row.image_height
        box_width = (row.x_max - row.x_min) / row.image_width
        box_height = (row.y_max - row.y_min) / row.image_height

        label_path.write_text(
            f"{class_label} {x_center} {y_center} {box_width} {box_height}"
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        list(
            tqdm(
                executor.map(process_dataset_row, labels.itertuples(index=False)),
                total=len(labels),
            )
        )

    labels.file = labels.apply(
        lambda row: Path(row.object_type) / Path(row.file), axis=1
    )
    labels.drop(columns="abs_file_path").to_csv(out_dir / "meta.csv", index=False)


def extract_boxes(
    label_paths: List[Path],
    out_dir: Path,
    only_pedestrians: bool,  # TODO: Rethink this
    box_size: Tuple[int, int],
):
    """Crop bounding boxes from a dataset on smirk format.

    Croped boxes will be resized to fit the specified box size.


    Args:
        label_paths: Paths to labels on smirk format.
        out_dir: Path to location for the extracted boxes.
        only_pedestrians: Only extract boxes containing pedestrians.
        box_size: Resize height and width.
    """
    labels = _load_labels_with_abs_path(label_paths)

    if only_pedestrians:
        labels = labels[labels.class_text == "pedestrian"]

    def _extract_box(row: Any):
        if row.class_text == "background":
            return None

        img_path = row.abs_file_path
        box_img = np.array(
            Image.open(img_path).crop((row.x_min, row.y_min, row.x_max, row.y_max))
        )
        box_img_letter = resize_box_img(box_img, box_size)

        save_path = out_dir / row.object_type / f"{row.run_id}-{img_path.name}"
        save_path.parent.mkdir(exist_ok=True, parents=True)
        Image.fromarray(box_img_letter).save(save_path)

        return save_path.relative_to(out_dir)

    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        paths = list(
            tqdm(
                executor.map(_extract_box, labels.itertuples()),
                total=len(labels),
            )
        )

    labels["file"] = paths

    labels.drop(columns="abs_file_path").to_csv(out_dir / "box-labels.csv", index=False)
