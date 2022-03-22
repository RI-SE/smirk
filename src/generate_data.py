import argparse
import itertools
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, Union, cast

from omegaconf import DictConfig, ListConfig, OmegaConf
from typing_extensions import Literal

import config.paths
from simple_aeb_scene import SimpleAebScene

MAX_RETRIES = 10


@dataclass
class PedestrianScenario:
    object = "pedestrian"
    type: Literal["left", "right", "towards", "away"]
    args: Tuple
    max_travel_distance: Optional[float] = None


@dataclass
class ObjectScenario:
    object = "object"
    type: Literal["left", "right"]
    args: Tuple
    max_travel_distance: Optional[float] = None


Scenario = Union[PedestrianScenario, ObjectScenario]


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


def step_until_end_condition(scenario: Scenario, scene: SimpleAebScene) -> None:
    max_travel_distance = scenario.max_travel_distance or float("inf")

    while True:
        scene.simulation.step(20)

        if (
            scene.has_object_crossed_road()
            or scene.get_object_distance_traveled() >= max_travel_distance
        ):
            return


def build_scenario_list(datagen_config: DictConfig):
    scenarios: List[Scenario] = []

    for scenario_config in datagen_config.scenarios:
        if scenario_config.get("pedestrian"):
            if scenario_config.type in ["left", "right"]:
                for scenario_args in get_pedestrian_left_right_args(scenario_config):
                    scenarios.append(
                        PedestrianScenario(
                            type=scenario_config.type,
                            args=scenario_args,
                            max_travel_distance=scenario_config.get(
                                "max_travel_distance"
                            ),
                        )
                    )
            elif scenario_config.type in ["towards", "away"]:
                for scenario_args in get_pedestrian_towards_away_args(scenario_config):
                    scenarios.append(
                        PedestrianScenario(
                            type=scenario_config.type,
                            args=scenario_args,
                            max_travel_distance=scenario_config.get(
                                "max_travel_distance"
                            ),
                        )
                    )
            else:
                raise ValueError(
                    f"Unknown pedestrian scenario type: {scenario_config.type}"
                )
        elif scenario_config.get("object"):
            for scenario_args in get_object_left_right_args(scenario_config):
                scenarios.append(
                    ObjectScenario(
                        type=scenario_config.type,
                        args=scenario_args,
                        max_travel_distance=scenario_config.get("max_travel_distance"),
                    )
                )
        else:
            raise ValueError(
                "Invalid scenario, expected object or pedestrian configuration."
            )

    return scenarios


def generate_data(config_path: Path) -> None:
    datagen_config = load_config(config_path)
    scenarios = build_scenario_list(datagen_config)
    scene = SimpleAebScene()

    for scenario in scenarios:
        for _ in range(MAX_RETRIES):
            try:
                if scenario.object == "pedestrian":
                    if scenario.type == "left":
                        scene.setup_scenario_pedestrian_from_left(*scenario.args)
                    elif scenario.type == "right":
                        scene.setup_scenario_pedestrian_from_right(*scenario.args)
                    elif scenario.type == "towards":
                        scene.setup_scenario_pedestrian_towards(*scenario.args)
                    elif scenario.type == "away":
                        scene.setup_scenario_pedestrian_away(*scenario.args)
                else:
                    if scenario.type == "left":
                        scene.setup_scenario_object_from_left(*scenario.args)
                    elif scenario.type == "right":
                        scene.setup_scenario_object_from_right(*scenario.args)

                step_until_end_condition(scenario, scene)
                break
            except ConnectionError:
                print("Prosivic crashed, restarting and retrying scenario.")
                subprocess.Popen([str(config.paths.prosivic_exe_path)])
                scene.reload()


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
