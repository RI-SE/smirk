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
def detect():
    """
    Training and evaluation of pedestrian detection models.

    Currently only YOLOv5.
    """
    pass


@detect.command()
@click.option(
    "--train",
    "train_path",
    type=click.Path(exists=True, file_okay=False, resolve_path=True, path_type=str),
    required=True,
    help="Path to training data directory",
)
@click.option(
    "--val",
    "val_path",
    type=click.Path(exists=True, file_okay=False, resolve_path=True, path_type=str),
    required=True,
    help="Path to validation data directory",
)
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(file_okay=False, resolve_path=True, path_type=str),
    required=True,
    help="Path to output directory.",
)
@click.option(
    "-h",
    "--hyper-parameters",
    "hyp",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=str),
    required=True,
    default=smirk.config.paths.yolo_model_hyp,
    help="Path to yolo hyper parameters file.",
)
@click.option("--epochs", type=int, default=10, help="Number of epoch to train")
@click.option("--batch-size", type=int, default=8, help="Batch size for training")
def train(
    train_path: str,
    val_path: str,
    output_path: str,
    hyp: str,
    epochs: int,
    batch_size: int,
):
    """
    Train pedestrian detection model.

    Currently mainly for SMIRK reproducibility purposes.
    """
    from smirk.adas.pedestrian_detector.yolo.train import run as train_yolo

    train_yolo(
        weights="",  # Train from scratch.
        cfg=smirk.config.paths.yolo_model_config,
        epochs=epochs,
        batch_size=batch_size,
        project=output_path,
        train_path=train_path,
        val_path=val_path,
        hyp=hyp,
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
    """Evalute pedestrian detection model.

    Currently mainly for SMIRK reproducibility purposes.
    """

    from smirk.adas.pedestrian_detector.yolo.val import evaluate

    evaluate(data_path, weights_path, conf, batch_size)
