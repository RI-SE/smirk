#
# SMIRK
# Copyright (C) 2021-2023 RISE Research Institutes of Sweden AB
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
import argparse
import random
from time import time

import nanoid
import numpy as np

import smirk.config.paths
from smirk.simulators.prosivic.scenes.simple_aeb_scene import SimpleAebScene
from smirk.tests.system.system_test_runner import (
    PedestrianTestConfiguration,
    SystemTestRunner,
)

SCENARIO_TYPES = ("left", "right", "towards", "away")
PEDESTRIAN_APPEARANCES = (
    "male_business",
    "male_casual",
    "male_construction",
    "female_business",
    "female_casual",
    "child",
)


def get_single_random_configuration(
    scenario_types=SCENARIO_TYPES,
    pedestrian_appearances=PEDESTRIAN_APPEARANCES,
    pedestrian_distance_from_car_range=(30, 150),
    pedestrian_walking_angle_range=(0, 180),
    pedestrian_distance_from_road_range=(-1, 2),
    pedestrian_walking_speed_range=(0, 2),
    pedestrian_offset_from_road_center_range=(-3, 3),
    car_speed_range=(2, 20),
) -> PedestrianTestConfiguration:
    scenario_type = random.choice(scenario_types)
    pedestrian_appearance = random.choice(pedestrian_appearances)
    car_speed = np.random.uniform(*car_speed_range)
    pedestrian_distance_from_car = np.random.uniform(
        *pedestrian_distance_from_car_range
    )
    pedestrian_distance_from_road = np.random.uniform(
        *pedestrian_distance_from_road_range
    )
    pedestrian_offset_from_road_center = np.random.uniform(
        *pedestrian_offset_from_road_center_range
    )
    pedestrian_walking_angle = np.random.uniform(*pedestrian_walking_angle_range)
    pedestrian_walking_speed = np.random.uniform(*pedestrian_walking_speed_range)

    scenario_id = nanoid.generate()

    if scenario_type == "left":
        return PedestrianTestConfiguration(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=pedestrian_distance_from_car,
            pedestrian_start_y=SimpleAebScene.ROAD_LEFT_Y
            + pedestrian_distance_from_road,
            pedestrian_angle=-pedestrian_walking_angle,
            pedestrian_speed=pedestrian_walking_speed,
            car_speed=car_speed,
            scenario_id=scenario_id,
        )
    elif scenario_type == "right":
        return PedestrianTestConfiguration(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=pedestrian_distance_from_car,
            pedestrian_start_y=SimpleAebScene.ROAD_RIGHT_Y
            - pedestrian_distance_from_road,
            pedestrian_angle=pedestrian_walking_angle,
            pedestrian_speed=pedestrian_walking_speed,
            car_speed=car_speed,
            scenario_id=scenario_id,
        )
    elif scenario_type == "towards":
        return PedestrianTestConfiguration(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=pedestrian_distance_from_car,
            pedestrian_start_y=pedestrian_offset_from_road_center,
            pedestrian_angle=180,
            pedestrian_speed=pedestrian_walking_speed,
            car_speed=car_speed,
            scenario_id=scenario_id,
        )
    elif scenario_type == "away":
        return PedestrianTestConfiguration(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=pedestrian_distance_from_car,
            pedestrian_start_y=pedestrian_offset_from_road_center,
            pedestrian_angle=0,
            pedestrian_speed=pedestrian_walking_speed,
            car_speed=car_speed,
            scenario_id=scenario_id,
        )

    raise Exception("Unknown scenario type")


def test_random_configurations(count: int):
    runner = SystemTestRunner(
        output_path=smirk.config.paths.temp_dir_path / f"{int(time())}_system_test"
    )

    runner.run_all(get_single_random_configuration() for _ in range(count))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--count", type=int, default=1, help="Number of scenarios to run."
    )
    args = parser.parse_args()

    test_random_configurations(count=args.count)
