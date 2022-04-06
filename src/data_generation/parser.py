import itertools
from pathlib import Path
from typing import List, Union, cast

from omegaconf import DictConfig, ListConfig, OmegaConf

from data_generation.scenario import (
    ObjectLeftRightArgs,
    ObjectLeftScenario,
    ObjectRightScenario,
    PedestrianAwayScenario,
    PedestrianLeftRightArgs,
    PedestrianLeftScenario,
    PedestrianRightScenario,
    PedestrianTowardsAwayArgs,
    PedestrianTowardsScenario,
    Scenario,
)


def ensure_list(value):
    if isinstance(value, ListConfig):
        return value

    return [value]


def parse_pedestrian_left_right_scenario(
    scenario_config: DictConfig,
) -> Union[List[PedestrianLeftScenario], List[PedestrianRightScenario]]:
    pedestrian_config = scenario_config.pedestrian
    car_speeds = [0]

    args_it = itertools.product(
        ensure_list(pedestrian_config.appearance),
        pedestrian_config.distances_from_car,
        pedestrian_config.distances_from_road,
        pedestrian_config.angles,
        pedestrian_config.speeds,
        car_speeds,
    )

    if scenario_config.type == "left":
        return [
            PedestrianLeftScenario(PedestrianLeftRightArgs(*args)) for args in args_it
        ]

    return [PedestrianRightScenario(PedestrianLeftRightArgs(*args)) for args in args_it]


def parse_pedestrian_towards_away_scenario(
    scenario_config: DictConfig,
) -> Union[List[PedestrianTowardsScenario], List[PedestrianAwayScenario]]:

    max_travel_distance = scenario_config.max_travel_distance
    pedestrian_config = scenario_config.pedestrian
    car_speeds = [0]

    args_it = itertools.product(
        ensure_list(pedestrian_config.appearance),
        pedestrian_config.distances_from_car,
        pedestrian_config.offsets_from_road_center,
        pedestrian_config.speeds,
        car_speeds,
    )

    if scenario_config.type == "towards":
        return [
            PedestrianTowardsScenario(
                PedestrianTowardsAwayArgs(*args),
                max_travel_distance=max_travel_distance,
            )
            for args in args_it
        ]

    return [
        PedestrianAwayScenario(
            PedestrianTowardsAwayArgs(*args), max_travel_distance=max_travel_distance
        )
        for args in args_it
    ]


def parse_object_left_right_scenario(
    scenario_config: DictConfig,
) -> Union[List[ObjectLeftScenario], List[ObjectRightScenario]]:
    object_config = scenario_config.object
    car_speeds = [0]

    args_it = itertools.product(
        ensure_list(object_config.type),
        object_config.distances_from_car,
        object_config.distances_from_road,
        object_config.speeds,
        car_speeds,
    )

    if scenario_config.type == "left":
        return [ObjectLeftScenario(ObjectLeftRightArgs(*args)) for args in args_it]

    return [ObjectRightScenario(ObjectLeftRightArgs(*args)) for args in args_it]


def build_scenario_list(config: DictConfig) -> List[Scenario]:
    scenarios: List[Scenario] = []

    for scenario_config in config.scenarios:
        if scenario_config.get("pedestrian"):
            if scenario_config.type in ["left", "right"]:
                scenarios.extend(parse_pedestrian_left_right_scenario(scenario_config))
            elif scenario_config.type in ["towards", "away"]:
                scenarios.extend(
                    parse_pedestrian_towards_away_scenario(scenario_config)
                )
            else:
                raise ValueError(
                    f"Unknown pedestrian scenario type: {scenario_config.type}"
                )
        elif scenario_config.get("object"):
            scenarios.extend(parse_object_left_right_scenario(scenario_config))
        else:
            raise ValueError(
                "Invalid scenario, expected object or pedestrian configuration."
            )

    return scenarios


def load_config(path: Path) -> DictConfig:
    if not OmegaConf.has_resolver("range"):
        OmegaConf.register_resolver(
            "range", lambda start, stop, step: range(int(start), int(stop), int(step))
        )
    cfg = OmegaConf.load(path)

    return cast(DictConfig, cfg)


def parse_scenario_config(path: Path):
    config = load_config(path)

    return build_scenario_list(config)
