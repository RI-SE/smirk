import math
from dataclasses import dataclass

import ProSivicDDS as psvdds

from simulators.prosivic.objects.pedestrian import Pedestrian
from simulators.prosivic.objects.position import Position
from simulators.prosivic.simulation import Simulation


@dataclass
class RawManObserverData:
    timestamp: float
    Speed: float
    Angle_X: float
    Angle_Y: float
    Angle_Z: float
    Human_coordinate_X: float
    Human_coordinate_Y: float
    Human_coordinate_Z: float


class ObservablePedestrian(Pedestrian):
    def __init__(self, name: str, observer_name: str, simulation: Simulation) -> None:
        super().__init__(name, simulation)
        self.observer = psvdds.manObserverHandler(observer_name)

    def get_observer_data(self) -> RawManObserverData:
        return self.observer.receive()

    def get_position(self) -> Position:
        """Returns current pedestrian position"""
        observer_data = self.get_observer_data()

        return Position(
            observer_data.Human_coordinate_X,
            observer_data.Human_coordinate_Y,
            observer_data.Human_coordinate_Z,
        )

    def get_walkling_angle(self):
        """Returns current pedestrian walking angle in degrees"""
        return round(math.degrees(self.get_observer_data().Angle_Z))
