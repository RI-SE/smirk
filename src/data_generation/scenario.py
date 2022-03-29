import dataclasses
from dataclasses import dataclass
from typing import Any, Optional, Union

from typing_extensions import Literal

import data_generation.utils
from simulators.prosivic.objects.pedestrian import PedestrianAppearance
from simulators.prosivic.objects.simple_object import SimpleObjectType


@dataclass
class Scenario:
    args: Any
    type: Literal["left", "right", "towards", "away"]
    object: Literal["pedestrian", "object"]
    id: str = dataclasses.field(
        default_factory=data_generation.utils.generate_scenario_id
    )
    max_travel_distance: Optional[float] = None

    def get_args_dict(self):
        args = dataclasses.asdict(self.args)

        return args


@dataclass
class PedestrianLeftRightArgs:
    pedestrian_appearance: PedestrianAppearance
    pedestrian_distance_from_car: float
    pedestrian_distance_from_road: float
    pedestrian_walking_angle: float
    pedestrian_walking_speed: float
    car_speed: float


@dataclass
class PedestrianTowardsAwayArgs:
    pedestrian_appearance: PedestrianAppearance
    pedestrian_distance_from_car: float
    pedestrian_offset_from_road_center: float
    pedestrian_walking_speed: float
    car_speed: float


@dataclass
class PedestrianScenario(Scenario):
    args: Union[PedestrianLeftRightArgs, PedestrianTowardsAwayArgs]
    type: Literal["left", "right", "towards", "away"]
    object: Literal["pedestrian"] = "pedestrian"


@dataclass
class PedestrianLeftScenario(PedestrianScenario):
    args: PedestrianLeftRightArgs
    type: Literal["left"] = "left"


@dataclass
class PedestrianRightScenario(PedestrianScenario):
    args: PedestrianLeftRightArgs
    type: Literal["right"] = "right"


@dataclass
class PedestrianTowardsScenario(PedestrianScenario):
    args: PedestrianTowardsAwayArgs
    type: Literal["towards"] = "towards"


@dataclass
class PedestrianAwayScenario(PedestrianScenario):
    args: PedestrianTowardsAwayArgs
    type: Literal["away"] = "away"


@dataclass
class ObjectLeftRightArgs:
    object_type: SimpleObjectType
    distance_from_car: float
    distance_from_road: float
    speed: float
    car_speed: float


@dataclass
class ObjectScenario(Scenario):
    args: ObjectLeftRightArgs
    type: Literal["left", "right"]
    object: Literal["object"] = "object"


@dataclass
class ObjectLeftScenario(ObjectScenario):
    args: ObjectLeftRightArgs
    type: Literal["left"] = "left"


@dataclass
class ObjectRightScenario(ObjectScenario):
    args: ObjectLeftRightArgs
    type: Literal["right"] = "right"
