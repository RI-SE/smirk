import argparse
import itertools
import sys
from pathlib import Path
from typing import cast

from omegaconf import DictConfig, ListConfig, OmegaConf

import config.paths
from simple_aeb_scene import SimpleAebScene


def load_config(config_path: Path) -> DictConfig:
    OmegaConf.register_resolver(
        "range", lambda start, stop, step: range(int(start), int(stop), int(step))
    )
    cfg = OmegaConf.load(config_path)

    return cast(DictConfig, cfg)


def ensure_list(value):
    if isinstance(value, ListConfig):
        return value

    return [value]


def get_pedestrian_left_right_args(scenario_config):
    pedestrian_config = scenario_config.pedestrian
    car_speeds = [0]

    return itertools.product(
        ensure_list(pedestrian_config.appearance),
        pedestrian_config.distances_from_car,
        pedestrian_config.distances_from_road,
        pedestrian_config.angles,
        pedestrian_config.speeds,
        car_speeds,
    )


def get_pedestrian_towards_away_args(scenario_config):
    pedestrian_config = scenario_config.pedestrian
    car_speeds = [0]

    return itertools.product(
        ensure_list(pedestrian_config.appearance),
        pedestrian_config.distances_from_car,
        pedestrian_config.offsets_from_road_center,
        pedestrian_config.speeds,
        car_speeds,
    )


def get_object_left_right_args(scenario_config):
    object_config = scenario_config.object
    car_speeds = [0]

    return itertools.product(
        ensure_list(object_config.type),
        object_config.distances_from_car,
        object_config.distances_from_road,
        object_config.speeds,
        car_speeds,
    )


def step_until_end_condition(
    scenario_config: DictConfig, scene: SimpleAebScene
) -> None:
    max_travel_distance = scenario_config.get("max_travel_distance", float("inf"))

    while True:
        scene.simulation.step(20)

        if (
            scene.has_object_crossed_road()
            or scene.get_object_distance_traveled() >= max_travel_distance
        ):
            return


def handle_pedestrian_scenario(scenario_config: DictConfig, scene: SimpleAebScene):
    if scenario_config.type == "left":
        for scenario_args in get_pedestrian_left_right_args(scenario_config):
            scene.setup_scenario_pedestrian_from_left(*scenario_args)
            step_until_end_condition(scenario_config, scene)
    elif scenario_config.type == "right":
        for scenario_args in get_pedestrian_left_right_args(scenario_config):
            scene.setup_scenario_pedestrian_from_right(*scenario_args)
            step_until_end_condition(scenario_config, scene)
    elif scenario_config.type == "towards":
        for scenario_args in get_pedestrian_towards_away_args(scenario_config):
            scene.setup_scenario_pedestrian_towards(*scenario_args)
            step_until_end_condition(scenario_config, scene)
    elif scenario_config.type == "away":
        for scenario_args in get_pedestrian_towards_away_args(scenario_config):
            scene.setup_scenario_pedestrian_away(*scenario_args)
            step_until_end_condition(scenario_config, scene)
    else:
        raise ValueError(f"Unknown pedestrian scenario type: {scenario_config.type}")


def handle_object_scenario(scenario_config: DictConfig, scene: SimpleAebScene):
    for scenario_args in get_object_left_right_args(scenario_config):
        if scenario_config.type == "left":
            scene.setup_scenario_object_from_left(*scenario_args)
        elif scenario_config.type == "right":
            scene.setup_scenario_object_from_left(*scenario_args)
        else:
            raise ValueError(f"Unknown object scenario type: {scenario_config.type}")

        step_until_end_condition(scenario_config, scene)


def generate_data(config_path: Path) -> None:
    config = load_config(config_path)
    scene = SimpleAebScene()

    for i, scenario_config in enumerate(config.scenarios):
        print(f"\nRunning configuration {i} type={scenario_config.type}")

        if scenario_config.get("pedestrian"):
            handle_pedestrian_scenario(scenario_config, scene)
        elif scenario_config.get("object"):
            handle_object_scenario(scenario_config, scene)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="path to config file")
    args = parser.parse_args()

    config_path = (
        Path(args.config)
        if args.config
        else Path(config.paths.example_data_generation_config)
    )

    if not config_path.exists():
        print(f"Could not find config: {config_path.absolute()}")
        sys.exit(-1)

    generate_data(config_path)
