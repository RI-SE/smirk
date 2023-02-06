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
from pathlib import Path
from time import time
from typing import Dict, Iterable, List, Union

import numpy as np
import pandas as pd
from omegaconf import OmegaConf
from PIL import Image
from pydantic.dataclasses import dataclass

from smirk.simulators.prosivic.scenes.simple_aeb_scene import SimpleAebScene
from smirk.simulators.prosivic.utils import TIMESTAMP_PER_SECOND


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
    RESULT_FILE_NAME = "results.csv"
    SUMMARY_FILE_NAME = "summary.csv"

    def __init__(
        self,
        output_path: Path,
        simulation_step_size=1,
        min_car_speed=0.1,
        add_noise=False,
    ):
        # NOTE: Speeds up cli.
        # TODO: Look for a better solution, lazy sub commands?.
        from smirk.adas.smirk import Smirk

        self.simulation_step_size = simulation_step_size
        self.min_car_speed = min_car_speed
        self.add_noise = add_noise

        self.scene = SimpleAebScene()
        self.smirk = Smirk()
        self.output_path = output_path
        self.output_path.mkdir(parents=True)

    def run_all(self, configurations: Iterable[SystemTestConfiguration]):
        for configuration in configurations:
            self.run_configuration(configuration)

    def add_noise_to_params(self, scenario_params: Dict):
        for k, v in scenario_params.items():
            if type(v) in [int, float]:
                scenario_params[k] = v * np.random.uniform(0.9, 1.1)

    def run_from_file(self, test_config: Path):
        cfg = OmegaConf.load(test_config)
        configurations: List[SystemTestConfiguration] = []

        for scenario in cfg.scenarios:
            if scenario.type == "pedestrian":
                configurations.append(
                    PedestrianTestConfiguration(**scenario.parameters)
                )
            elif scenario.type == "object":
                configurations.append(ObjectTestConfiguration(**scenario.parameters))
            else:
                raise Exception("Unknown scenario type")

        self.run_all(configurations)
        self.create_result_summary()

    def run_configuration(self, test_config: SystemTestConfiguration):
        results: List[Dict] = []

        param_dict = dataclasses.asdict(test_config)

        scenario_save_dir = self.output_path / test_config.scenario_id
        scenario_save_dir.mkdir(parents=True)

        if self.add_noise:
            self.add_noise_to_params(param_dict)

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

                result_path = scenario_save_dir / self.RESULT_FILE_NAME
                pd.DataFrame(results).to_csv(result_path, index=False)

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

    def create_result_summary(self):
        result_paths = self.output_path.glob(f"**/{self.RESULT_FILE_NAME}")

        results = pd.concat([pd.read_csv(p) for p in result_paths], ignore_index=True)

        results.radar_data_timestamp = (
            results.radar_data_timestamp / TIMESTAMP_PER_SECOND
        ).round(1)
        results.camera_data_timestamp = (
            results.camera_data_timestamp / TIMESTAMP_PER_SECOND
        ).round(1)
        results.radar_triggered = results.radar_triggered.fillna(False)
        results.brake = results.brake.fillna(False)

        distance = results.groupby("scenario_id").distance.min()
        radar_trigger_time = (
            results[results.radar_triggered]
            .groupby("scenario_id")
            .radar_data_timestamp.min()
        )
        brake_trigger_time = (
            results[results.brake].groupby("scenario_id").radar_data_timestamp.min()
        )
        radar_trigger_distance = results.loc[
            results[results.radar_triggered]
            .groupby("scenario_id")
            .radar_data_timestamp.idxmin()
        ].distance
        brake_trigger_distance = results.loc[
            results[results.brake].groupby("scenario_id").radar_data_timestamp.idxmin()
        ].distance
        collision = results.groupby("scenario_id").is_collision.any()
        collision_speed = (
            results[results.is_collision]
            .groupby("scenario_id")
            .first()
            .current_car_speed
        )

        pd.DataFrame(
            {
                "Min distance": distance,
                "Radar trigger time": radar_trigger_time,
                "Brake trigger time": brake_trigger_time,
                "Radar trigger distance": pd.Series(
                    radar_trigger_distance.tolist(), index=radar_trigger_time.index
                ),
                "Brake trigger distance": pd.Series(
                    brake_trigger_distance.tolist(), index=brake_trigger_time.index
                ),
                "Collision": collision,
                "Collision speed": collision_speed,
                "Initial speed": results.groupby("scenario_id").first().car_speed,
            }
        ).to_csv(self.output_path / self.SUMMARY_FILE_NAME, index=False)
