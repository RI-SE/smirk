from dataclasses import dataclass
from uuid import uuid4

import ProSivicDDS as psvdds

from simulators.prosivic.objects.position import Position
from simulators.prosivic.simulation import Simulation


@dataclass
class RawObjectObserverData:
    """Approximation of prosivic objectObserver data."""

    timestamp: int
    position_x: float
    position_y: float
    position_z: float
    angle_x: float
    angle_y: float
    angle_z: float
    speed: float
    direction_x: float
    direction_y: float
    direction_z: float


class ObjectObserver:
    def __init__(self, simulation: Simulation) -> None:
        self.simulation = simulation
        self.name = str(uuid4())
        self.simulation.create_object("sivicObjectObserver", self.name, dds=True)
        self.observer = psvdds.objectObserverHandler(self.name)

    def set_object(self, object_name):
        self.simulation.cmd(f"{self.name}.SetObject {object_name}")

    def get_observation(self) -> RawObjectObserverData:
        return self.observer.receive()

    def get_position(self) -> Position:
        """Returns current object position"""
        observer_data = self.get_observation()

        return Position(
            observer_data.position_x,
            observer_data.position_y,
            observer_data.position_z,
        )

    def delete(self) -> None:
        self.simulation.delete_object(self.name)
