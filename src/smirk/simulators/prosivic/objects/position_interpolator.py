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
from uuid import uuid4

from smirk.simulators.prosivic.simulation import Simulation


class PositionInterpolator:
    PROSIVIC_OBJECT_NAME = "mgPositionInterpolator"

    def __init__(self, simulation: Simulation) -> None:
        self.simulation: Simulation = simulation
        self.name = str(uuid4())
        self.simulation.create_object(self.PROSIVIC_OBJECT_NAME, self.name)

    def set_controlled_object(self, controlled_object_name: str) -> None:
        self.simulation.cmd(f"{self.name}.SetTarget {controlled_object_name}")

    def set_seconds_between_frames(self, seconds: float) -> None:
        self.simulation.cmd(f"{self.name}.SetPeriod {seconds}")

    def add_key_frame(
        self,
        x: float = 0,
        y: float = 0,
        z: float = 0,
        rotation_x: float = 0,
        rotation_y: float = 0,
        rotation_z: float = 0,
    ) -> None:
        self.simulation.cmd(
            f"{self.name}.AddKeyFrame {x} {y} {z} {rotation_x} {rotation_y} {rotation_z}"
        )

    def play(self) -> None:
        self.simulation.cmd(f"{self.name}.Play")

    def delete(self) -> None:
        self.simulation.delete_object(self.name)
