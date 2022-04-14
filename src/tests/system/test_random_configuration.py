import argparse
import random

import nanoid
import numpy as np

from simple_aeb_scene import SimpleAebScene
from tests.system.system_test_runner import (
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
    runner = SystemTestRunner()
    runner.run_all(get_single_random_configuration() for _ in range(count))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--count", type=int, default=1, help="Number of scenarios to run."
    )
    args = parser.parse_args()

    test_random_configurations(count=args.count)
