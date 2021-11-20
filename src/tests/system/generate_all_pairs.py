"""
TODO: This is all tigthly and implicitly coupled to the simple_aeb_scene! It makes a number of implicit assumptions about angles, object positions, coordinate system etc. Try to at least make that more explicit.
"""
from collections import OrderedDict
from random import shuffle
from typing import Any, List, Sequence, Tuple, Union, cast

import numpy as np
from allpairspy import AllPairs

from tests.system.system_test_runner import SystemTestConfiguration

Interval = Tuple[float, float]

# Equivalence classes
latteral_offset_mapping = dict(right=-5, center=0, left=5)
pedestrian_speed_mapping = dict(stationary=0, slow=1, fast=3)
pedestrian_angle_mapping = dict(
    away=0, diagonal_away=45, perpendicular=90, diagonal_towards=135, towards=180
)
pedestrian_distance_mapping = {
    "close": (5, 25),
    "medium": (25, 50),
    "far": (50, 100),
}
car_speed_mapping = {
    "slow": (3, 9),
    "medium": (10, 15),
    "fast": (15, 20),
}


test_parameters = OrderedDict(
    {
        "pedestrian_start_y": [
            "left",
            "center",
            "right",
        ],
        "pedestrian_start_x": [
            "close",
            "medium",
            "far",
        ],
        "pedestrian_speed": [
            "stationary",
            "slow",
            "fast",
        ],
        "pedestrian_angle": [
            "away",
            "diagonal_away",
            "perpendicular",
            "diagonal_towards",
            "towards",
        ],
        "car_speed": [
            "slow",
            "medium",
            "fast",
        ],
        "pedestrian_appearance": [
            "child",
            "female_business",
            "female_casual",
            "male_business",
            "male_casual",
            "male_worker",
        ],
    }
)


def get_overlapping_interval(a: Interval, b: Interval) -> Union[Interval, None]:
    [a_start, a_end] = a
    [b_start, b_end] = b

    if a_start > b_end or b_start > a_end:
        return None

    return (max(a_start, b_start), min(a_end, b_end))


def get_random_int_on_interval(interval: Interval) -> int:
    [start, end] = interval
    start_ceil = int(np.ceil(start))
    end_floor = int(np.floor(end))

    if start_ceil == end_floor:
        return start_ceil

    if start_ceil > end or end_floor < start:
        raise Exception("Too tight interval")

    return np.random.randint(start_ceil, end_floor)


def calculate_collision_values(
    start_y_category: str,
    start_x_category: str,
    pedestrian_speed_category: str,
    pedestrian_angle_category: str,
    car_speed_category: str,
    pedestrian_appearance="",
    collision_offsets: List[float] = None,
    latteral_offset_paddings: Sequence[int] = (0, -1, 1),
):
    if collision_offsets is None:
        collision_offsets = [-0.5, 0, 0.5]
    shuffle(collision_offsets)

    pedestrian_y0 = latteral_offset_mapping[start_y_category]
    pedestrian_speed = pedestrian_speed_mapping[pedestrian_speed_category]
    pedestrian_angle = pedestrian_angle_mapping[pedestrian_angle_category]
    pedestrian_x0_interval = pedestrian_distance_mapping[start_x_category]
    car_speed_interval = car_speed_mapping[car_speed_category]

    if start_y_category == "center" and (
        pedestrian_speed_category == "stationary"
        or pedestrian_angle_category in ["towards", "away"]
    ):
        return SystemTestConfiguration(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=get_random_int_on_interval(pedestrian_x0_interval),
            pedestrian_start_y=pedestrian_y0,
            pedestrian_angle=pedestrian_angle,
            pedestrian_speed=pedestrian_speed,
            car_speed=get_random_int_on_interval(car_speed_interval),
        )

    elif start_y_category in ["left", "right"] and (
        pedestrian_speed == "stationary" or pedestrian_angle in ["away", "towards"]
    ):
        return None

    # Angle relative perpendicular
    pedestrian_angle_perp_rad = np.deg2rad(90 - pedestrian_angle)
    # Pedestrian speed perpendicular to road
    pedestrian_v_y = pedestrian_speed * np.cos(pedestrian_angle_perp_rad)
    # Pedestrian speed paralell to road
    pedestrian_v_x = pedestrian_speed * np.sin(pedestrian_angle_perp_rad)

    for offset_padding in latteral_offset_paddings:
        for collision_offset in collision_offsets:
            pedestrian_y0_padded = pedestrian_y0 + offset_padding
            pedestrian_delta_y = abs(pedestrian_y0_padded) + collision_offset
            delta_t = pedestrian_delta_y / pedestrian_v_y
            pedestrian_delta_x = pedestrian_v_x * delta_t

            pedestrian_x1_interval = pedestrian_delta_x + np.array(
                pedestrian_x0_interval
            )
            car_x1_interval = delta_t * np.array(car_speed_interval)

            overlapping_interval = get_overlapping_interval(
                pedestrian_x1_interval, car_x1_interval
            )

            if overlapping_interval is None:
                continue

            x_collision = get_random_int_on_interval(overlapping_interval)
            pedestrian_x0 = x_collision - pedestrian_delta_x
            car_v = x_collision / delta_t

            if start_y_category == "left":
                pedestrian_angle = -pedestrian_angle

            if start_y_category == "center":
                pedestrian_angle = (
                    pedestrian_angle if np.random() > 0.5 else -pedestrian_angle
                )

            return SystemTestConfiguration(
                pedestrian_appearance=pedestrian_appearance,
                pedestrian_start_x=pedestrian_x0,
                pedestrian_start_y=pedestrian_y0_padded,
                pedestrian_angle=pedestrian_angle,
                pedestrian_speed=np.round(pedestrian_speed, 2),
                car_speed=np.round(car_v, 2),
            )

    return None


def is_valid_combination(row) -> bool:
    n = len(row)

    [
        pedestrian_start_y,
        pedestrian_start_x,
        pedestrian_speed,
        pedestrian_angle,
        car_speed,
        _,
    ] = row + [None] * (6 - n)

    if pedestrian_start_y in ["left", "right"] and (
        pedestrian_speed == "stationary" or pedestrian_angle in ["away", "towards"]
    ):
        return False

    if n >= 5 and not calculate_collision_values(
        pedestrian_start_y,
        pedestrian_start_x,
        pedestrian_speed,
        pedestrian_angle,
        car_speed,
    ):
        return False

    return True


for pair in AllPairs(test_parameters, filter_func=is_valid_combination):
    pair = cast(Any, pair)
    print(
        calculate_collision_values(
            start_y_category=pair.pedestrian_start_y,
            start_x_category=pair.pedestrian_start_x,
            pedestrian_speed_category=pair.pedestrian_speed,
            pedestrian_angle_category=pair.pedestrian_angle,
            car_speed_category=pair.car_speed,
            pedestrian_appearance=pair.pedestrian_appearance,
        )
    )
