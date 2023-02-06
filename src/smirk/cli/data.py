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
from pathlib import Path
from typing import List, Tuple

import click
import pandas as pd

import smirk.config.paths
import smirk.data.utils


@click.group()
def data():
    """
    Data pre-processing.
    Utilities for splitting and transforming generated data.
    """
    pass


@data.command()
@click.option(
    "-l",
    "--labels",
    "label_paths",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    multiple=True,
    required=True,
    help="Path to labels file. Pass multiple times to include multiple.",
)
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(file_okay=False, resolve_path=True, path_type=Path),
    required=False,
    default=smirk.config.paths.default_data_dir_path,
    help="Path to output directory.",
)
# TODO: Better place for default values
@click.option("--seed", type=int, default=3, help="Random seed to use for splitting.")
@click.option(
    "--val_size", type=float, default=0.2, help="Fraction of data to use for validation"
)
def split(
    label_paths: List[Path],
    output_path: Path,
    seed: int,
    val_size: float,
):
    """Split a dataset on smirk format into a train and val set."""
    output_path.mkdir(exist_ok=True, parents=True)
    split_result = smirk.data.utils.split(label_paths, val_size, seed)

    pd.Series(list(split_result.val_ids)).to_csv(
        output_path / "val_ids.txt", header=False, index=False
    )
    pd.Series(list(split_result.train_ids)).to_csv(
        output_path / "train_ids.txt", header=False, index=False
    )


@data.command()
@click.option(
    "-l",
    "--labels",
    "label_paths",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    multiple=True,
    required=True,
    help="Path to labels file. Pass multiple times to include multiple.",
)
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(file_okay=False, resolve_path=True, path_type=Path),
    required=False,
    default=smirk.config.paths.default_data_dir_path,
    help="Path to output directory.",
)
@click.option(
    "--subset",
    "subset_path",
    type=click.Path(dir_okay=False, resolve_path=True, path_type=Path),
    required=True,
    help="Path to file specifying subset of run ids to use e.g. output from split.",
)
def convert(label_paths: List[Path], output_path: Path, subset_path: Path = None):
    """
    Convert a dataset on smirk format to another format.
    NOTE: Might require admin priviliges to run.

    Currently only yolo is supported.
    """

    include_ids = None
    if subset_path is not None:
        include_ids = pd.read_csv(subset_path, header=None, squeeze=True)
        if not isinstance(include_ids, pd.Series):
            raise Exception("Invalid subset file")

    smirk.data.utils.to_yolo(label_paths, output_path, include_ids)


@data.command()
@click.option(
    "-l",
    "--labels",
    "label_paths",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=Path,
    ),
    multiple=True,
    required=True,
    help="Path to labels file. Pass multiple times to include multiple.",
)
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(file_okay=False, resolve_path=True, path_type=Path),
    required=False,
    default=smirk.config.paths.default_data_dir_path,
    help="Path to output directory.",
)
@click.option(
    "--only-pedestrians",
    is_flag=True,
    default=False,
    help="Only extract pedestrian bounding boxes.",
)
@click.option(
    "--box-size",
    required=False,
    nargs=2,
    type=int,
    default=(160, 64),  # TODO: extract
    help="Extracted box dimensions (height,width).",
)
def extract_boxes(
    label_paths: List[Path],
    output_path: Path,
    only_pedestrians: bool,  # TODO: Rethink how this is handled.
    box_size: Tuple[int, int],
):
    """Crop bounding boxes from a dataset on smirk format.

    Creates a new dataset containing only the contents of the bounding boxes. Boxes are resized to the specified dimensions.
    """

    smirk.data.utils.extract_boxes(label_paths, output_path, only_pedestrians, box_size)
