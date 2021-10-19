import math
from dataclasses import dataclass
from uuid import uuid4

import ProSivicDDS as psvdds

from simulators.prosivic.objects.position import Position
from simulators.prosivic.simulation import Simulation


@dataclass
class RawManObserverData:
    """Approximation of prosivic manObserver data."""

    timestamp: float
    Speed: float
    Angle_X: float
    Angle_Y: float
    Angle_Z: float
    Human_coordinate_X: float
    Human_coordinate_Y: float
    Human_coordinate_Z: float


class PedestrianObserver:
    def __init__(self, simulation: Simulation) -> None:
        self.simulation = simulation
        self.name = str(uuid4())
        self.simulation.create_object("sivicManObserver", self.name, dds=True)
        self.observer = psvdds.manObserverHandler(self.name)

    def set_object(self, object_name):
        self.simulation.cmd(f"{self.name}.SetObject {object_name}")

    def get_observation(self) -> RawManObserverData:
        return self.observer.receive()

    def get_position(self) -> Position:
        """Returns current pedestrian position"""
        observer_data = self.get_observation()

        return Position(
            observer_data.Human_coordinate_X,
            observer_data.Human_coordinate_Y,
            observer_data.Human_coordinate_Z,
        )

    def get_walkling_angle(self) -> int:
        """Returns current pedestrian walking angle in degrees"""
        return round(math.degrees(self.get_observation().Angle_Z))

    def delete(self) -> None:
        self.simulation.delete_object(self.name)
