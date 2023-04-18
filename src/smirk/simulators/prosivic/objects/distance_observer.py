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
from dataclasses import dataclass

from smirk.simulators.prosivic.objects.position import Position
from smirk.simulators.prosivic.simulation import Simulation

from ..psvdds import psvdds


@dataclass
class _RawProsivicData:
    """Approximation of the object returned from prosivic distance observer."""

    timestamp: int
    position_object1_x: float
    position_object1_y: float
    position_object1_z: float
    position_object2_x: float
    position_object2_y: float
    position_object2_z: float
    distance: float


@dataclass
class DistanceObserverData:
    timestamp: int
    position_object1: Position
    position_object2: Position
    distance: float


class DistanceObserver:
    def __init__(
        self,
        simulation: Simulation,
        name: str,
    ) -> None:
        self.simulation = simulation
        self.name = name
        self.observer = psvdds.distanceObserverHandler(self.name)

    def set_object1(self, object_name: str) -> None:
        self.simulation.cmd(f"{self.name}.SetObject1 {object_name}")

    def set_object2(self, object_name: str) -> None:
        self.simulation.cmd(f"{self.name}.SetObject2 {object_name}")

    def get_data(self) -> DistanceObserverData:
        data: _RawProsivicData = self.observer.receive()

        return DistanceObserverData(
            timestamp=data.timestamp,
            position_object1=Position(
                data.position_object1_x,
                data.position_object1_y,
                data.position_object1_z,
            ),
            position_object2=Position(
                data.position_object2_x,
                data.position_object2_y,
                data.position_object2_z,
            ),
            distance=data.distance,
        )

    def get_position_object1(self) -> Position:
        return self.get_data().position_object1

    def get_position_object2(self) -> Position:
        return self.get_data().position_object2

    def get_distance(self) -> float:
        return self.get_data().distance
