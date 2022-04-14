import dataclasses
import math
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Union, cast

import numpy as np
import pandas as pd

from simple_aeb_scene import SimpleAebScene
from smirk.smirk import Smirk


@dataclass
class ObjectTestConfiguration:
    object_type: str
    start_x: float
    start_y: float
    end_x: float
    end_y: float
    angle: float
    speed: float
    car_speed: float
    scenario_id: str


@dataclass
class PedestrianTestConfiguration:
    pedestrian_appearance: str
    pedestrian_start_x: float
    pedestrian_start_y: float
    pedestrian_angle: float
    pedestrian_speed: float
    car_speed: float
    scenario_id: str


SystemTestConfiguration = Union[PedestrianTestConfiguration, ObjectTestConfiguration]


DEFAULT_CONFIG = dict(simulation_step_size=1, min_car_speed=0.1)


class SystemTestRunner:
    def __init__(self, config=DEFAULT_CONFIG):
        self.config = config
        self.scene = SimpleAebScene()
        self.smirk = Smirk()
        self.results: List[Dict] = []

    def results_to_csv(self):
        path = f"system_test_results_{datetime.now():%Y%m%d_%H%M%S}.csv"
        pd.DataFrame(self.results).to_csv(path)

    def run_all(
        self, configurations: Iterable[SystemTestConfiguration], add_noise: bool = False
    ):
        for configuration in configurations:
            self.run_configuration(configuration, add_noise)

    def run_configuration(self, test_config: SystemTestConfiguration, add_noise: bool):
        param_dict = dataclasses.asdict(test_config)

        if add_noise:
            for k, v in param_dict.items():
                if type(v) in [int, float]:
                    param_dict[k] *= 1 + np.random.uniform(-0.1, 0.1)
                    print(k, v, param_dict[k])

        if isinstance(test_config, PedestrianTestConfiguration):
            self.scene.setup_pedestrian_scenario(**param_dict)
        elif isinstance(test_config, ObjectTestConfiguration):
            self.scene.setup_object_scenario(**param_dict)
        else:
            raise Exception("Invalid system test config")

        result = dict(
            min_distance=math.inf,
            timestamp_ttc_triggered=None,
            distance_ttc_triggered=None,
            timestamp_aeb_triggered=None,
            distance_aeb_triggered=None,
            collision=False,
            car_end_speed=None,
        )

        is_braking = False
        prev_radar_data = self.scene.radar.get_detections()

        while True:
            self.scene.simulation.step(self.config["simulation_step_size"])

            collision_data = self.scene.get_collision_data()
            car_speed = self.scene.car.get_speed()

            result["min_distance"] = min(
                cast(float, result["min_distance"]), collision_data.distance
            )

            if (
                collision_data.has_car_passed_object
                or collision_data.is_collision
                or car_speed < self.config["min_car_speed"]
            ):
                result["collision"] = collision_data.is_collision
                result["car_end_speed"] = car_speed

                self.results.append({**param_dict, **result})
                return

            if is_braking:
                continue

            radar_data = self.scene.radar.get_detections()
            is_new_radar_data_available = (
                prev_radar_data.timestamp != radar_data.timestamp
            )

            if is_new_radar_data_available:
                prev_radar_data = radar_data
                camera_data = self.scene.camera.get_frame()
                min_ttc = min(
                    [detection.ttc for detection in radar_data.detections],
                    default=math.inf,
                )

                if (
                    result["distance_ttc_triggered"] is None
                    and min_ttc < self.smirk.TTC_THRESHOLD_SECONDS
                ):
                    result["distance_ttc_triggered"] = collision_data.distance
                    result["timestamp_ttc_triggered"] = radar_data.timestamp

                if result["distance_aeb_triggered"] is None and self.smirk.is_aeb(
                    radar_data.detections, camera_data.frame_data
                ):
                    result["distance_aeb_triggered"] = collision_data.distance
                    result["timestamp_aeb_triggered"] = camera_data.timestamp

                    self.scene.car.brake()
                    is_braking = True
