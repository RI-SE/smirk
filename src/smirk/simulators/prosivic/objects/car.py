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
from enum import Enum
from typing import List

import smirk.simulators.prosivic.utils as utils
from smirk.simulators.prosivic.simulation import Simulation

from ..psvdds import psvdds


class CruiseControlPositions(Enum):
    NoControl = 0
    SpeedControl = 1
    SpeedLimit = 2


class Car:
    def __init__(self, simulation: Simulation, name: str) -> None:
        self.name = name
        self.simulation = simulation
        self.order_handler = psvdds.carOrderHandler(name)
        self.environment_handler = psvdds.carEnvironmentHandler(name)

    def set_init_speed(self, speed_ms: float) -> None:
        speed_kmh = utils.ms_to_kmh(speed_ms)
        self.simulation.cmd(f"{self.name}.SetInitSpeed {speed_kmh}")

    def set_cruise_control(self, speed_ms: float) -> None:
        speed_kmh = utils.ms_to_kmh(speed_ms)
        self.simulation.cmd(
            f"{self.name}.SetCruiseControlPosition {CruiseControlPositions.SpeedControl.value}"
        )
        self.simulation.cmd(f"{self.name}.SetInitSpeedControl {speed_kmh}")
        self.simulation.cmd(f"{self.name}.SetSpeedControl {speed_kmh}")

    def brake(self) -> None:
        order = self.order_handler.receive()
        order.movementOrderMode = psvdds.emovementOrder.pedals
        order.cruiseControlPosition = psvdds.ecruiseControl.off
        order.brake = 1
        self.order_handler.transmit(order)

    def get_speed(self) -> float:
        # TODO: Return undocumented in manual. Assauming list of speeds along the cars axis [x,y,z].
        #       Could also be along world axis?
        #       Seems to be in ms whereas other car values tend to be in kmh.
        speed_ms: List[float] = self.environment_handler.receive().speed

        return speed_ms[0]
