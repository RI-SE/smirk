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
from pathlib import Path

import click

import smirk.config.paths


@click.group()
def safety():
    """
    Outlier detection training and evaluation. Currently only SMIRK AE Box model
    """


@safety.command()
@click.option(
    "-d",
    "--data",
    "data_path",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
    help="Path to directory with extracted bouding boxes.",
)
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(file_okay=False, resolve_path=True, path_type=Path),
    required=True,
    help="Path to output directory.",
)
@click.option("--epochs", type=int, default=30, help="Number of epoch to train")
@click.option("--batch-size", type=int, default=1024, help="Batch size for training")
# TODO: Customization + Better place for default values
def train(data_path: Path, output_path: Path, epochs: int, batch_size: int):
    """Train outlier detector."""
    from smirk.adas.safety_cage.ae_box.train import train as trian_ae_box

    trian_ae_box(
        data_path,
        output_path,
        epochs,
        batch_size,
        seed=3,
        img_height=160,
        img_width=64,
        num_channels=3,
        encoding_dim=1024,
    )


@safety.command()
@click.option(
    "-d",
    "--data",
    "data_path",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    required=True,
    help="Path to pedestrian_detector results pickle",
)
@click.option(
    "-w",
    "--weights",
    "weights_path",
    type=click.Path(exists=True, file_okay=False, resolve_path=True, path_type=Path),
    required=True,
    default=smirk.config.paths.ae_box_model,
    help="Path to model",
)
@click.option("--batch-size", type=int, default=1000, help="Batch size")
def eval_outlier(data_path: Path, weights_path: Path, batch_size: int):
    """
    Evalute outlier detector in isolation.
    """
    from smirk.adas.safety_cage.ae_box.eval_outlier import (
        evaluate_outlier as ae_box_eval,
    )

    ae_box_eval(data_path, weights_path, batch_size)


@safety.command()
@click.option(
    "-d",
    "--data",
    "data_path",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    required=True,
    help="Path to ae box evaluation results pickle",
)
@click.option(
    "--conf", type=float, required=True, help="Pedestrian detector confidence threshold"
)
@click.option("--outlier", type=float, required=True, help="Outlier score threshold")
@click.option("--distance", type=float, default=0, help="Distance threshold")
def eval_with_detector(data_path: Path, conf: float, outlier: float, distance: float):
    """
    Evalute outlier detector together with pedestrian detector.
    """
    from smirk.adas.safety_cage.ae_box.eval_with_detector import (
        eval_with_detector as ae_box_eval_with_detector,
    )

    ae_box_eval_with_detector(data_path, conf, outlier, distance)
