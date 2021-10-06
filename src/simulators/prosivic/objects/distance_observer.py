from dataclasses import dataclass

import ProSivicDDS as psvdds

from simulators.prosivic.objects.position import Position
from simulators.prosivic.simulation import Simulation


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
