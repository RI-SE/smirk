import dataclasses
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
from typing_extensions import Literal

import data_generation.utils
from simulators.prosivic.objects.pedestrian import PedestrianAppearance
from simulators.prosivic.objects.simple_object import SimpleObjectType


@dataclass
class ScenarioCameraFrame:
    path: Path
    index: int
    width: int
    height: int
    bounding_box: Union[Tuple[int, int, int, int], None]

    def is_occluded(self) -> bool:
        x_min, y_min, x_max, y_max = self.bounding_box or [None] * 4

        return any((x_min == 0, y_min == 0, x_max == self.width, y_max == self.height))

    def to_label_dict(self):
        x_min, y_min, x_max, y_max = self.bounding_box or [None] * 4
        return dict(
            file=self.path.as_posix(),
            frame_index=self.index,
            image_width=self.width,
            image_height=self.height,
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
            is_occluded=self.is_occluded(),
        )


@dataclass
class ScenarioResults:
    camera_frames: List[ScenarioCameraFrame]
    distance_data: pd.DataFrame  # Prosivic distance observer csv

    def get_distance_at_frame_index(self, index):
        loc = min(index - 1, self.distance_data.index[-1])

        return self.distance_data.at[loc, "Distance(m)"]

    def to_label_list(self) -> List[Dict[str, Any]]:

        return [
            dict(
                **frame.to_label_dict(),
                current_distance=self.get_distance_at_frame_index(frame.index)
            )
            for frame in self.camera_frames
        ]


@dataclass
class Scenario:
    args: Any
    type: Literal["left", "right", "towards", "away"]
    object: Literal["pedestrian", "object"]
    id: str = dataclasses.field(
        default_factory=data_generation.utils.generate_scenario_id
    )
    max_travel_distance: Optional[float] = None
    results: Optional[ScenarioResults] = None

    def get_args_dict(self):
        args = dataclasses.asdict(self.args)
        args["scenario_id"] = self.id

        return args

    def to_label_rows(self) -> List[Dict[str, Any]]:
        base = dict(
            run_id=self.id,
            scenario_type=self.type,
        )

        if not self.results or not self.results.camera_frames:
            raise Exception("No results available.")

        return [
            dict(
                **result,
                class_text=self.object if result["x_min"] is not None else "background",
                **base
            )
            for result in self.results.to_label_list()
        ]


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

    def to_label_rows(self) -> List[Dict[str, Any]]:
        args = self.get_args_dict()

        addition = dict(
            object_type=self.args.pedestrian_appearance,
            start_distance_from_car=self.args.pedestrian_distance_from_car,
            speed=self.args.pedestrian_walking_speed,
            angle=args.get("pedestrian_walking_angle"),
            offset_from_road_center=args.get("pedestrian_offset_from_road_center"),
        )

        return [{**base, **addition} for base in super().to_label_rows()]


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

    def to_label_rows(self) -> List[Dict[str, Any]]:
        addition = dict(
            object_type=self.args.object_type,
            start_distance_from_car=self.args.distance_from_car,
            speed=self.args.speed,
            angle=90,  # HACK: Always 90 for now but hard to catch a change...
            offset_from_road_center=None,
        )

        return [{**base, **addition} for base in super().to_label_rows()]


@dataclass
class ObjectLeftScenario(ObjectScenario):
    args: ObjectLeftRightArgs
    type: Literal["left"] = "left"


@dataclass
class ObjectRightScenario(ObjectScenario):
    args: ObjectLeftRightArgs
    type: Literal["right"] = "right"
