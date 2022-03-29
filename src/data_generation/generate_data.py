import argparse
import sys
from pathlib import Path

import config.paths as paths
import data_generation.parser
from data_generation.scenario import (
    ObjectLeftScenario,
    ObjectRightScenario,
    PedestrianAwayScenario,
    PedestrianLeftScenario,
    PedestrianRightScenario,
    PedestrianTowardsScenario,
    Scenario,
)
from simple_aeb_scene import SimpleAebScene


def step_until_end_condition(scenario: Scenario, scene: SimpleAebScene) -> None:
    max_travel_distance = scenario.max_travel_distance or float("inf")

    while True:
        scene.simulation.step(20)

        if (
            scene.has_object_crossed_road()
            or scene.get_object_distance_traveled() >= max_travel_distance
        ):
            return


def generate_data(config_path: Path) -> None:
    scene = SimpleAebScene()
    scenarios = data_generation.parser.parse_scenario_config(config_path)

    for scenario in scenarios:
        scenario_args = scenario.get_args_dict()
        if isinstance(scenario, PedestrianLeftScenario):
            scene.setup_scenario_pedestrian_from_left(**scenario_args)
        elif isinstance(scenario, PedestrianRightScenario):
            scene.setup_scenario_pedestrian_from_right(**scenario_args)
        elif isinstance(scenario, PedestrianTowardsScenario):
            scene.setup_scenario_pedestrian_towards(**scenario_args)
        elif isinstance(scenario, PedestrianAwayScenario):
            scene.setup_scenario_pedestrian_away(**scenario_args)
        elif isinstance(scenario, ObjectLeftScenario):
            scene.setup_scenario_object_from_left(**scenario_args)
        elif isinstance(scenario, ObjectRightScenario):
            scene.setup_scenario_object_from_right(**scenario_args)

        step_until_end_condition(scenario, scene)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="path to config file")
    args = parser.parse_args()

    config_path = (
        Path(args.config) if args.config else Path(paths.example_data_generation_config)
    )

    if not config_path.exists():
        print(f"Could not find config: {config_path.absolute()}")
        sys.exit(-1)

    generate_data(config_path)
