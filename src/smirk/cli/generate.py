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
from smirk.data_generation.generate_data import generate_data


@click.command()
@click.option(
    "--psv-exe",
    "prosivic_exe_path",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path),
    required=True,
    help="Path to prosivic executable.",
)
@click.option(
    "--psv-sensors",
    "prosivic_sensors_path",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, resolve_path=True, path_type=Path
    ),
    required=True,
    help="Path to prosivic sensors output dir.",
)
@click.option(
    "-c",
    "--config",
    "config_path",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, resolve_path=True, path_type=Path
    ),
    required=True,
    help="Path to data generation config file.",
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
    "-r",
    "--resume",
    is_flag=True,
    default=False,
    help="Resume previous run of the config file.",
)
def generate(
    prosivic_exe_path: Path,
    prosivic_sensors_path: Path,
    config_path: Path,
    output_path: Path,
    resume: bool,
):
    """
    Data generation
    """
    generate_data(
        prosivic_exe_path,
        prosivic_sensors_path,
        config_path,
        output_path,
        resume,
    )
