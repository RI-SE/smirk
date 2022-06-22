#
# SMIRK
# Copyright (C) 2021-2022 RISE Research Institutes of Sweden AB
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import dataclasses
from dataclasses import dataclass
from datetime import datetime
from time import time
from typing import Dict, Iterable, List, Union

import numpy as np
import pandas as pd
from PIL import Image

from adas.smirk import Smirk
from config import paths
from simple_aeb_scene import SimpleAebScene


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


class SystemTestRunner:
    def __init__(self, simulation_step_size=1, min_car_speed=0.1):
        self.simulation_step_size = simulation_step_size
        self.min_car_speed = min_car_speed

        self.scene = SimpleAebScene()
        self.smirk = Smirk()
        self.img_save_dir = (
            paths.project_root_path / "system_test" / f"{datetime.now():%Y%m%d_%H%M%S}"
        )
        self.img_save_dir.mkdir(parents=True)

    def run_all(
        self, configurations: Iterable[SystemTestConfiguration], add_noise: bool = False
    ):
        for configuration in configurations:
            self.run_configuration(configuration, add_noise)

    def add_noise(self, scenario_params: Dict):
        for k, v in scenario_params.items():
            if type(v) in [int, float]:
                scenario_params[k] = v * np.random.uniform(0.9, 1.1)

    def run_configuration(self, test_config: SystemTestConfiguration, add_noise: bool):
        results: List[Dict] = []

        param_dict = dataclasses.asdict(test_config)

        scenario_save_dir = self.img_save_dir / test_config.scenario_id
        scenario_save_dir.mkdir(parents=True)

        if add_noise:
            self.add_noise(param_dict)

        if isinstance(test_config, PedestrianTestConfiguration):
            self.scene.setup_pedestrian_scenario(**param_dict)
        elif isinstance(test_config, ObjectTestConfiguration):
            self.scene.setup_object_scenario(**param_dict)
        else:
            raise Exception("Invalid system test config")

        is_braking = False
        prev_radar_data = None

        while True:
            self.scene.simulation.step(self.simulation_step_size)

            collision_data = self.scene.get_collision_data()
            car_speed = self.scene.car.get_speed()

            if (
                collision_data.has_car_passed_object
                or collision_data.is_collision
                or car_speed < self.min_car_speed
            ):
                results.append(
                    dict(
                        is_end=True,
                        current_car_speed=car_speed,
                        is_collision=collision_data.is_collision,
                        distance=collision_data.distance,
                        **param_dict,
                    )
                )

                result_path = scenario_save_dir / "results.csv"
                pd.DataFrame(results).to_csv(result_path)

                return

            if is_braking:
                results.append(
                    dict(
                        is_end=False,
                        is_braking=is_braking,
                        current_car_speed=car_speed,
                        is_collision=collision_data.is_collision,
                        distance=collision_data.distance,
                        **param_dict,
                    )
                )
                continue

            radar_data = self.scene.radar.get_detections()
            is_new_radar_data_available = (
                not prev_radar_data
            ) or prev_radar_data.timestamp != radar_data.timestamp

            if is_new_radar_data_available:
                prev_radar_data = radar_data

                camera_data = self.scene.camera.get_frame()
                t0 = time()
                smirk_res = self.smirk.is_aeb(
                    radar_data.detections, camera_data.frame_data
                )
                smirk_time = time() - t0

                if smirk_res.radar:
                    camera_img_path = (
                        scenario_save_dir / f"{camera_data.timestamp}_frame.png"
                    )
                    Image.fromarray(camera_data.frame_data).save(camera_img_path)

                    bbox_img_path = None
                    if smirk_res.bbox_img is not None:
                        bbox_img_path = (
                            scenario_save_dir / f"{camera_data.timestamp}_bbox.png"
                        )

                        Image.fromarray(smirk_res.bbox_img).save(bbox_img_path)

                    results.append(
                        dict(
                            is_end=False,
                            is_braking=is_braking,
                            brake=smirk_res.brake,
                            radar_triggered=smirk_res.radar,
                            pedestrian_detected=smirk_res.camera,
                            radar_camera_fusion=smirk_res.radar_camera_fusion,
                            safety_cage_accept=smirk_res.cage,
                            camera_img_path=camera_img_path,
                            bbox_img_path=bbox_img_path,
                            predicted_bbox=None
                            if smirk_res.bbox is None
                            else dataclasses.astuple(smirk_res.bbox),
                            radar_data_timestamp=radar_data.timestamp,
                            distance=collision_data.distance,
                            camera_data_timestamp=radar_data.timestamp,  # Use radar time as reference
                            current_car_speed=car_speed,
                            is_collision=collision_data.is_collision,
                            execution_time=smirk_time,
                            **param_dict,
                        )
                    )

                    if smirk_res.brake:
                        self.scene.car.brake()
                        is_braking = True
