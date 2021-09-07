from enum import Enum
from typing import List

import ProSivicDDS as psvdds

from simulators.prosivic.simulation import Simulation


class CruiseControlPositions(Enum):
    NoControl = 0
    SpeedControl = 1
    SpeedLimit = 2


class Car:
    def __init__(self, name: str, simulation: Simulation) -> None:
        self.name = name
        self.simulation = simulation
        self.order_handler = psvdds.carOrderHandler(name)
        self.environment_handler = psvdds.carEnvironmentHandler(name)

    # Doesn't work in Prosivic 2020
    # def set_speed(self, speed: float) -> None:
    #     self.simulation.cmd(f"{self.name}.SetSpeed {speed}")

    def set_init_speed(self, speed: float) -> None:
        self.simulation.cmd(f"{self.name}.SetInitSpeed {speed}")

    def set_cruise_control(self, speed: float) -> None:
        self.simulation.cmd(
            f"{self.name}.SetCruiseControlPosition {CruiseControlPositions.SpeedControl.value}"
        )
        self.simulation.cmd(f"{self.name}.SetInitSpeedControl {speed}")
        self.simulation.cmd(f"{self.name}.SetSpeedControl {speed}")

    def brake(self) -> None:
        order = psvdds.carOrder()
        order.movementOrderMode = psvdds.emovementOrder.pedals
        order.brake = 1
        self.order_handler.transmit(order)

    def ms_to_kmh(self, speed: float) -> float:
        return speed * (3600 / 1000)

    def get_speed(self) -> float:
        speed: List[float] = self.environment_handler.receive().speed

        return self.ms_to_kmh(speed[0])
