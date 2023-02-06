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
import click

from smirk.cli.data import data
from smirk.cli.detect import detect
from smirk.cli.generate import generate
from smirk.cli.safety import safety
from smirk.cli.test import test
from smirk.simulators.prosivic.psvdds import is_psv_dds_available

from . import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

if not is_psv_dds_available():
    click.secho(
        "NOTE: ProSivicDDS is not available. Simulation features will not work.\n",
        fg="red",
    )


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(
    __version__,
    "--version",
    "-v",
)
def main():
    """
    Experimental pedestrian emergency breaking ADAS facilitating research on quality assurance of critical components that rely on machine learning.
    """
    pass


main.add_command(generate)
main.add_command(detect)
main.add_command(safety)
main.add_command(test)
main.add_command(data)
