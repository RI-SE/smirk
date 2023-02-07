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
import pickle
import shutil
from pathlib import Path
from time import sleep
from typing import List, Optional, cast

import pandas as pd
from PIL import Image

import smirk.config.paths as paths
import smirk.data_generation.parser as datagen_parser
from smirk.data_generation.scenario import (
    ObjectLeftScenario,
    ObjectRightScenario,
    PedestrianAwayScenario,
    PedestrianLeftScenario,
    PedestrianRightScenario,
    PedestrianTowardsScenario,
    Scenario,
    ScenarioCameraFrame,
    ScenarioResults,
)
from smirk.simulators.prosivic.scenes.simple_aeb_scene import SimpleAebScene
from smirk.simulators.prosivic.supervisor import Supervisor

# TODO: Refactor: Extract class

MAX_SCENARIO_RETRIES = 10
MIN_EXPECTED_FRAMES = 10
LABELS_FILENAME = "labels.csv"


class DirCountException(Exception):
    pass


class NotEnoughFramesException(Exception):
    pass


def step_until_end_condition(scenario: Scenario, scene: SimpleAebScene) -> None:
    max_travel_distance = scenario.max_travel_distance or float("inf")

    while True:
        scene.simulation.step(20)

        if (
            scene.has_object_crossed_road()
            or scene.get_object_distance_traveled() >= max_travel_distance
        ):
            return


def find_scenario_dir(id: str, prosivic_sensor_dir: Path) -> Optional[Path]:
    # PERF: Use prosivic session name to reduce files we need to search.
    search_res = sorted(prosivic_sensor_dir.glob(f"**/*{id}"))

    if not search_res:
        return None

    if len(search_res) > 1:
        raise DirCountException(
            f"Unexpected number of scenario out dirs, found {len(search_res)}"
        )

    return search_res[0]


def read_scenario_data_from_disk(
    scenario_id: str,
    result_dir: Path,
    prosivic_sensor_dir: Path,
    scene: SimpleAebScene,
    img_ext="png",
):
    """Read scenario data prosivic writes to disk."""
    out_dir = find_scenario_dir(scenario_id, prosivic_sensor_dir)

    if not out_dir:
        raise Exception(f"Could not find out dir for {scenario_id}")

    new_path = result_dir / scenario_id

    if out_dir != new_path:
        for attempt in range(3):
            try:
                out_dir.rename(new_path)
                break
            except Exception as e:
                sleep(0.1)
                if attempt == 2:
                    raise e

    mask_paths = sorted(new_path.glob(f"*labels.{img_ext}"))
    camera_frames: List[ScenarioCameraFrame] = []

    for index, mask_path in enumerate(mask_paths, start=1):
        with Image.open(mask_path) as im:
            width, height = im.size
            bbox = im.getbbox()

        frame_path = (
            mask_path.with_name(mask_path.stem)
            .with_suffix(f".{img_ext}")
            .relative_to(result_dir)
        )

        camera_frames.append(
            ScenarioCameraFrame(
                path=frame_path,
                index=index,
                width=width,
                height=height,
                bounding_box=bbox,
            )
        )

    distance_data = pd.read_csv(
        new_path / scene.COLLISION_OBSERVER_OUTPUT, sep=";", comment="%"
    )

    return ScenarioResults(camera_frames, distance_data)


def delete_scenario_dir(scenario_id: str, prosivic_sensor_dir: Path):
    scenario_dir = find_scenario_dir(scenario_id, prosivic_sensor_dir)

    if scenario_dir:
        shutil.rmtree(scenario_dir)


def create_result_dir(name: str, data_dir: Path, resume: bool) -> Path:
    result_dir = data_dir / name

    if not resume and result_dir.exists():
        raise Exception(
            f"Data for the {name} configuration already exists. Try resuming it instead."
        )

    result_dir.mkdir(exist_ok=resume, parents=True)

    return result_dir


def get_pickle_path_from_config(config_path: Path) -> Path:
    return paths.temp_dir_path / f"{config_path.stem}-scenarios.pickle"


def read_scenarios_pickle(config_path: Path):
    with get_pickle_path_from_config(config_path).open("rb") as f:
        return cast(List[Scenario], pickle.load(f))


def write_scenario_pickle(config_path: Path, scenarios: List[Scenario]):
    with get_pickle_path_from_config(config_path).open("wb") as f:
        pickle.dump(scenarios, f)


def is_scenario_generated(scenario_id: str, result_dir: Path):
    return (result_dir / scenario_id).exists()


def setup_scenario_in_scene(scenario: Scenario, scene: SimpleAebScene):
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
    else:
        raise ValueError(f"Unexpected scenario type {scenario}")


def generate_data(
    prosivic_exe_path: Path,
    prosivic_sensor_dir: Path,
    config_path: Path,
    output_path: Path,
    resume: bool,
) -> None:
    prosivic_supervisor = Supervisor(prosivic_exe_path)
    scene = SimpleAebScene()

    if resume:
        scenarios = read_scenarios_pickle(config_path)
    else:
        scenarios = datagen_parser.parse_scenario_config(config_path)
        write_scenario_pickle(config_path, scenarios)

    result_rows = []
    result_dir = create_result_dir(
        name=config_path.stem, data_dir=output_path, resume=resume
    )

    for scenario in scenarios:
        for _ in range(MAX_SCENARIO_RETRIES):
            try:
                if not is_scenario_generated(scenario.id, result_dir):
                    setup_scenario_in_scene(scenario, scene)
                    step_until_end_condition(scenario, scene)

                    # Make sure prosivic disk lock is released
                    scene.simulation.stop()

                scenario.results = read_scenario_data_from_disk(
                    scenario.id, result_dir, prosivic_sensor_dir, scene
                )

                # TODO: Better way to check if scenario is not complete?
                #       Seems to have at most 1-2 frames when this happens.
                if len(scenario.results.camera_frames) < MIN_EXPECTED_FRAMES:
                    raise NotEnoughFramesException("Too few frames...")

                result_rows.extend(scenario.to_label_rows())

                break
            except Exception as e:  # Try to catch (almost) everything prosivic throws our way...
                print(e)
                print(f"Retrying scenario {scenario}")

                prosivic_supervisor.restart()
                scene.reload()
                delete_scenario_dir(scenario.id, prosivic_sensor_dir)

    pd.DataFrame(result_rows).to_csv(result_dir / LABELS_FILENAME, index=False)
