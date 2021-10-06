import argparse
import math
import random
from datetime import datetime
from typing import Any, Dict, List, cast

import numpy as np
import pandas as pd

from simple_aeb_scene import SimpleAebScene
from smirk.pedestrian_detector.ssd_hub_detector import SsdHubDetector
from smirk.safety_cage.noop_cage import NoopCage
from smirk.smirk import Smirk

SCENARIO_TYPES = ("left", "right", "towards", "away")
PEDESTRIAN_APPEARANCES = (
    "male_business",
    "male_casual",
    "male_construction",
    "female_business",
    "female_casual",
    "child",
)


def get_random_parameters(
    scenario_types=SCENARIO_TYPES,
    pedestrian_appearances=PEDESTRIAN_APPEARANCES,
    pedestrian_distance_from_car_range=(30, 150),
    pedestrian_walking_angle_range=(0, 180),
    pedestrian_distance_from_road_range=(-1, 2),
    pedestrian_walking_speed_range=(0, 2),
    pedestrian_offset_from_road_center_range=(-3, 3),
    car_speed_range=(30, 70),
):
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

    if scenario_type in ["left", "right"]:
        return (
            scenario_type,
            dict(
                pedestrian_appearance=pedestrian_appearance,
                pedestrian_distance_from_car=pedestrian_distance_from_car,
                pedestrian_walking_speed=pedestrian_walking_speed,
                pedestrian_walking_angle=pedestrian_walking_angle,
                pedestrian_distance_from_road=pedestrian_distance_from_road,
                car_speed=car_speed,
            ),
        )

    return (
        scenario_type,
        dict(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_distance_from_car=pedestrian_distance_from_car,
            pedestrian_offset_from_road_center=pedestrian_offset_from_road_center,
            pedestrian_walking_speed=pedestrian_walking_speed,
            car_speed=car_speed,
        ),
    )


def setup_scenario(
    scene: SimpleAebScene, scenario_type: str, parameters: Dict[Any, Any]
) -> None:
    if scenario_type == "left":
        scene.setup_scenario_walk_from_left(**parameters)
    if scenario_type == "right":
        scene.setup_scenario_walk_from_right(**parameters)
    if scenario_type == "towards":
        scene.setup_scenario_walk_towards(**parameters)
    if scenario_type == "away":
        scene.setup_scenario_walk_away(**parameters)


def step_until_end_condition(scene: SimpleAebScene, smirk: Smirk):
    result = dict(
        min_distance=math.inf,
        timestamp_ttc_triggered=None,
        distance_ttc_triggered=None,
        timestamp_aeb_triggered=None,
        distance_aeb_triggered=None,
        collision=False,
        car_end_speed=None,
    )

    prev_radar_data = scene.radar.get_detections()

    while True:
        scene.simulation.step(1)

        collision_data = scene.get_collision_data()
        car_speed = scene.car.get_speed()

        result["min_distance"] = min(
            cast(float, result["min_distance"]), collision_data.distance
        )

        if (
            collision_data.has_car_passed_pedestrian
            or collision_data.is_collision
            or car_speed < 0.1
        ):
            result["collision"] = collision_data.is_collision
            result["car_end_speed"] = car_speed

            return result

        radar_data = scene.radar.get_detections()
        is_new_radar_data_available = prev_radar_data.timestamp != radar_data.timestamp

        if is_new_radar_data_available:
            prev_radar_data = radar_data
            camera_data = scene.camera.get_frame()
            min_ttc = min(
                [detection.ttc for detection in radar_data.detections], default=math.inf
            )

            if (
                result["distance_ttc_triggered"] is None
                and min_ttc < smirk.TTC_THRESHOLD_SECONDS
            ):
                result["distance_ttc_triggered"] = collision_data.distance
                result["timestamp_ttc_triggered"] = radar_data.timestamp

            if result["distance_aeb_triggered"] is None and smirk.is_aeb(
                min_ttc, camera_data.frame_data
            ):
                result["distance_aeb_triggered"] = collision_data.distance
                result["timestamp_aeb_triggered"] = camera_data.timestamp
                scene.car.brake()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--count", type=int, default=1, help="Number of scenarios to run."
    )
    args = parser.parse_args()

    scene = SimpleAebScene()
    smirk = Smirk(pedestrian_detector=SsdHubDetector(), safety_cage=NoopCage())

    results: List[Dict] = []

    for _ in range(args.count):
        scenario_type, scenario_parameters = get_random_parameters()
        setup_scenario(scene, scenario_type, scenario_parameters)
        scenario_result = step_until_end_condition(scene, smirk)

        results.append(
            {"scenario_type": scenario_type, **scenario_parameters, **scenario_result}
        )

    pd.DataFrame(results).to_csv(
        f"random_run_results_{datetime.now():%Y%m%d_%H%M%S}.csv"
    )
