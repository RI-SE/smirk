import ProSivicDDS as psvdds

from pedestrian_generator.prosivic.simulation import Simulation
from pedestrian_generator.prosivic.objects.pedestrian import Pedestrian
from pedestrian_generator.prosivic.objects.position import Position


class ObservablePedestrian(Pedestrian):
    def __init__(self, name: str, observer_name: str, simulation: Simulation) -> None:
        super().__init__(name, simulation)
        self.observer = psvdds.manObserverHandler(observer_name)

    def getPosition(self) -> Position:
        observer_data = self.observer.receive()

        return Position(
            observer_data.Human_coordinate_X,
            observer_data.Human_coordinate_Y,
            observer_data.Human_coordinate_Z,
        )
