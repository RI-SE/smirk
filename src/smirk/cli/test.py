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
from smirk.tests.system.system_test_runner import SystemTestRunner


@click.command()
@click.option(
    "-c",
    "--config",
    "config_path",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False, resolve_path=True, path_type=Path
    ),
    default=smirk.config.paths.default_system_test_config,
    help="Path to system test config file.",
)
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(file_okay=False, resolve_path=True, path_type=Path),
    help="Path to output directory.",
)
@click.option(
    "-n",
    "--noisy",
    is_flag=True,
    default=False,
    help="Add random jitter in the range from -10%% to +10%% to all numerical values.",
)
def test(config_path: Path, output_path: Path, noisy: bool):
    """
    System simulator testing.
    """
    runner = SystemTestRunner(output_path, add_noise=noisy)
    runner.run_from_file(config_path)
