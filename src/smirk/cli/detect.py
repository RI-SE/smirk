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

import click

import smirk.config.paths
from smirk.adas.pedestrian_detector.yolo.val import evaluate


@click.group()
def detect():
    """
    Training and evaluation of pedestrian detection models. Currently only YOLOv5.
    """
    pass


@detect.command()
def train():
    """
    Train pedestrian detection model.
    """
    click.secho(
        "WIP: Simple training is not yet available. Use model from release page for now.",
        fg="yellow",
    )


@detect.command()
@click.option(
    "-d",
    "--data",
    "data_path",
    type=click.Path(exists=True, file_okay=False, resolve_path=True, path_type=Path),
    required=True,
    help="Path to dataset directory",
)
@click.option(
    "-w",
    "--weights",
    "weights_path",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    required=True,
    default=smirk.config.paths.yolo_model,
    help="Path to model weights",
)
@click.option("--conf", type=float, required=True, help="Confidence threshold")
@click.option("--batch-size", type=int, default=256, help="Batch size")
def eval(data_path: Path, weights_path: Path, conf: float, batch_size: int):
    """
    Evalute pedestrian detection model.
    """
    evaluate(data_path, weights_path, conf, batch_size)
