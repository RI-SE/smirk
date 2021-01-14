import itertools
from pathlib import Path
from typing import cast

from omegaconf import OmegaConf, DictConfig


from pedestrian_generator.direction import Direction
from pedestrian_generator.prosivic.objects.observable_pedestrian import (
    ObservablePedestrian,
)
from pedestrian_generator.prosivic.simulation import Simulation
from pedestrian_generator.utils.timer import Timer


FEMALE_PEDESTRIAN_NAME = "female/pedestrian"
FEMALE_PEDESTRIAN_OBSERVER = "female_observer"


def load_config(config_path: Path) -> DictConfig:
    OmegaConf.register_resolver(
        "range", lambda start, stop, step: range(int(start), int(stop), int(step))
    )
    cfg = OmegaConf.load(config_path)

    return cast(DictConfig, cfg)


def main(config_path: Path) -> None:
    cfg = load_config(config_path)
    simulation = Simulation(cfg.script)
    female_pedestrian = ObservablePedestrian(
        FEMALE_PEDESTRIAN_NAME, FEMALE_PEDESTRIAN_OBSERVER, simulation
    )

    timer = Timer()

    for direction, distance, angle, speed in itertools.product(
        cfg.pedestrian.directions,
        cfg.pedestrian.distances,
        cfg.pedestrian.angles,
        cfg.pedestrian.speeds,
    ):
        if direction == Direction.left:
            start_position_y = cfg.left_y
            end_position_y = cfg.right_y
            direction_angle = -angle
        else:
            start_position_y = cfg.right_y
            end_position_y = cfg.left_y
            direction_angle = angle

        print(
            f"\nRunning configuration start={start_position_y}, end={end_position_y}, distance={distance}, angle={angle}, speed={speed}"
        )
        timer.start()

        run_scenario_configuration(
            simulation,
            start_position_y,
            end_position_y,
            female_pedestrian,
            distance,
            direction_angle,
            speed,
        )

        print(f"DONE: {timer.stop():0.2f}s")


def run_scenario_configuration(
    simulation: Simulation,
    start_position_y: int,
    end_position_y: int,
    pedestrian: ObservablePedestrian,
    distance: int,
    angle: int,
    speed: int,
) -> None:

    # TODO: Does z=0 work in all situations?
    pedestrian.set_position(distance, start_position_y, 0)
    pedestrian.set_angle(angle)

    simulation.play()

    pedestrian.set_speed(speed)

    # TODO: Some scenarios get skipped? Do we need to wait for postion to be set?
    wait_for_end_condition(start_position_y, end_position_y, pedestrian)

    simulation.pause()


def wait_for_end_condition(
    start_position_y: int, end_position_y: int, pedestrian: ObservablePedestrian
) -> None:
    is_increasing = start_position_y < end_position_y

    if is_increasing:
        while pedestrian.getPosition().y < end_position_y:
            pass
    else:
        while pedestrian.getPosition().y > end_position_y:
            pass
