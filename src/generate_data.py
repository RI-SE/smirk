import argparse
import itertools
import sys
from pathlib import Path
from typing import cast

from omegaconf import DictConfig, OmegaConf

import utils.paths
from simple_aeb_scene import SimpleAebScene


def load_config(config_path: Path) -> DictConfig:
    OmegaConf.register_resolver(
        "range", lambda start, stop, step: range(int(start), int(stop), int(step))
    )
    cfg = OmegaConf.load(config_path)

    return cast(DictConfig, cfg)


def get_left_right_args(scenario_config):
    pedestrian_config = scenario_config.pedestrian
    car_speeds = [0]

    return itertools.product(
        pedestrian_config.distances_from_car,
        pedestrian_config.distances_from_road,
        pedestrian_config.angles,
        pedestrian_config.speeds,
        car_speeds,
    )


def get_towards_away_args(scenario_config):
    pedestrian_config = scenario_config.pedestrian
    car_speeds = [0]

    return itertools.product(
        pedestrian_config.distances_from_car,
        pedestrian_config.offsets_from_road_center,
        pedestrian_config.speeds,
        car_speeds,
    )


def step_until_end_condition(
    scenario_config: DictConfig, scene: SimpleAebScene
) -> None:
    max_walking_distance = scenario_config.pedestrian.get(
        "max_walking_distance", float("inf")
    )

    while True:
        scene.simulation.step(20)

        if (
            scene.has_pedestrian_crossed_road()
            or scene.get_pedestrian_distance_walked() >= max_walking_distance
        ):
            return


def generate_data(config_path: Path) -> None:
    config = load_config(config_path)
    scene = SimpleAebScene()

    for i, scenario_config in enumerate(config.scenarios):
        print(f"\nRunning configuration {i} type={scenario_config.type}")
        if scenario_config.type == "left":
            for scenario_args in get_left_right_args(scenario_config):
                scene.setup_scenario_walk_from_left(*scenario_args)
                step_until_end_condition(scenario_config, scene)
        elif scenario_config.type == "right":
            for scenario_args in get_left_right_args(scenario_config):
                scene.setup_scenario_walk_from_right(*scenario_args)
                step_until_end_condition(scenario_config, scene)
        elif scenario_config.type == "towards":
            for scenario_args in get_towards_away_args(scenario_config):
                scene.setup_scenario_walk_towards(*scenario_args)
                step_until_end_condition(scenario_config, scene)
        elif scenario_config.type == "away":
            for scenario_args in get_towards_away_args(scenario_config):
                scene.setup_scenario_walk_away(*scenario_args)
                step_until_end_condition(scenario_config, scene)
        else:
            raise ValueError(f"Unknown scenario type {scenario_config.type}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="path to config file")
    args = parser.parse_args()

    config_path = (
        Path(args.config)
        if args.config
        else Path(utils.paths.example_data_generation_config)
    )

    if not config_path.exists():
        print(f"Could not find config: {config_path.absolute()}")
        sys.exit(-1)

    generate_data(config_path)
