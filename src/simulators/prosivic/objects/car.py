from enum import Enum
from typing import List

import ProSivicDDS as psvdds

import simulators.prosivic.utils as utils
from simulators.prosivic.simulation import Simulation


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
        order = psvdds.carOrder()
        order.movementOrderMode = psvdds.emovementOrder.pedals
        order.brake = 1
        self.order_handler.transmit(order)

    def get_speed(self) -> float:
        # TODO: Return undocumented in manual. Assauming list of speeds along the cars axis [x,y,z].
        #       Could also be along world axis?
        #       Seems to be in ms whereas other car values tend to be in kmh.
        speed_ms: List[float] = self.environment_handler.receive().speed

        return speed_ms[0]
