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
"""
TODO: This is all tigthly and implicitly coupled to the simple_aeb_scene! It makes a number of implicit assumptions about angles, object positions, coordinate system etc. Try to at least make that more explicit.
"""
import random
from collections import OrderedDict
from typing import Any, Sequence, Tuple, Union, cast

import numpy as np
from allpairspy import AllPairs

from smirk.tests.system.system_test_runner import (
    ObjectTestConfiguration,
    PedestrianTestConfiguration,
)

Interval = Tuple[float, float]


# Equivalence classes
latteral_offset_mapping = dict(right=-5, center=0, left=5)
object_speed_mapping = dict(stationary=0, slow=1, fast=3)
object_distance_mapping = {
    "close": (5, 25),
    "medium": (25, 50),
    "far": (50, 100),
}
object_angle_mapping = dict(
    away=0, diagonal_away=45, perpendicular=90, diagonal_towards=135, towards=180
)
car_speed_mapping = {
    "slow": (3, 9),
    "medium": (10, 15),
    "fast": (15, 20),
}


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
    start_y_class: str,
    start_x_class: str,
    obj_speed_class: str,
    obj_angle_class: str,
    car_speed_class: str,
    collision_offsets: Sequence[float] = (-0.5, 0, 0.5),
    latteral_offset_paddings: Sequence[int] = (0, -1, 1),
):
    if start_y_class in ["left", "right"] and (
        obj_speed_class == "stationary" or obj_angle_class in ["away", "towards"]
    ):
        return None

    obj_y0 = latteral_offset_mapping[start_y_class]
    obj_speed = object_speed_mapping[obj_speed_class]
    obj_angle = object_angle_mapping[obj_angle_class]

    obj_x0_interval = object_distance_mapping[start_x_class]
    car_speed_interval = car_speed_mapping[car_speed_class]

    if start_y_class == "center" and (
        obj_speed_class == "stationary" or obj_angle_class in ["towards", "away"]
    ):
        return get_random_int_on_interval(obj_x0_interval), get_random_int_on_interval(
            car_speed_interval
        )

    # Angle relative perpendicular
    obj_angle_perp_rad = np.deg2rad(90 - obj_angle)
    # Object speed perpendicular to road
    obj_vy = obj_speed * np.cos(obj_angle_perp_rad)
    # Object speed paralell to road
    obj_vx = obj_speed * np.sin(obj_angle_perp_rad)

    collision_offsets = list(collision_offsets)
    random.shuffle(collision_offsets)

    for offset_padding in latteral_offset_paddings:
        for collision_offset in collision_offsets:
            obj_y0_padded = obj_y0 + offset_padding
            obj_delta_y = abs(obj_y0_padded) + collision_offset
            delta_t = obj_delta_y / obj_vy
            obj_delta_x = obj_vx * delta_t

            obj_x1_interval = obj_delta_x + np.array(obj_x0_interval)
            car_x1_interval = delta_t * np.array(car_speed_interval)

            overlapping_interval = get_overlapping_interval(
                obj_x1_interval, car_x1_interval
            )

            if overlapping_interval is None:
                continue

            x_collision = get_random_int_on_interval(overlapping_interval)
            obj_x0 = x_collision - obj_delta_x
            car_v = x_collision / delta_t

            return obj_x0, np.round(car_v, 2)

    return None


def is_valid_combination(row) -> bool:
    n_params = len(row)

    [start_y, start_x, obj_speed, obj_angle, car_speed, _] = row + [None] * (
        6 - n_params
    )

    if start_y in ["left", "right"] and (
        obj_speed == "stationary" or obj_angle in ["away", "towards"]
    ):
        return False

    if n_params >= 5 and not calculate_collision_values(
        start_y,
        start_x,
        obj_speed,
        obj_angle,
        car_speed,
    ):
        return False

    return True


def generate_object_all_pairs():
    test_parameters = OrderedDict(
        {
            "obj_start_y": [
                "left",
                "right",
            ],
            "obj_start_x": [
                "close",
                "medium",
                "far",
            ],
            "obj_speed": [
                "stationary",
                "slow",
                "fast",
            ],
            "obj_angle": [
                "perpendicular",
            ],
            "car_speed": [
                "slow",
                "medium",
                "fast",
            ],
            "obj_type": [
                "box",
                "cone",
                "pyramid",
                "sphere",
            ],
        }
    )

    for pair in AllPairs(test_parameters, filter_func=is_valid_combination):
        pair = cast(Any, pair)
        collision_values = calculate_collision_values(
            start_y_class=pair.obj_start_y,
            start_x_class=pair.obj_start_x,
            obj_speed_class=pair.obj_speed,
            obj_angle_class=pair.obj_angle,
            car_speed_class=pair.car_speed,
        )

        if not collision_values:
            raise Exception("Expected collision values to exists")

        obj_x0, car_speed = collision_values
        obj_y0 = latteral_offset_mapping[pair.obj_start_y]

        print(
            ObjectTestConfiguration(
                object_type=pair.obj_type,
                start_x=obj_x0,
                start_y=obj_y0,
                end_x=obj_x0,
                end_y=-obj_y0,
                angle=-np.sign(obj_y0) * 90,
                speed=object_speed_mapping[pair.obj_speed],
                car_speed=car_speed,
            )
        )


def generate_pedestrian_all_pairs():
    test_parameters = OrderedDict(
        {
            "obj_start_y": [
                "left",
                "center",
                "right",
            ],
            "obj_start_x": [
                "close",
                "medium",
                "far",
            ],
            "obj_speed": [
                "stationary",
                "slow",
                "fast",
            ],
            "obj_angle": [
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
                "male_construction",
            ],
        }
    )

    for pair in AllPairs(test_parameters, filter_func=is_valid_combination):
        pair = cast(Any, pair)
        collision_values = calculate_collision_values(
            start_y_class=pair.obj_start_y,
            start_x_class=pair.obj_start_x,
            obj_speed_class=pair.obj_speed,
            obj_angle_class=pair.obj_angle,
            car_speed_class=pair.car_speed,
        )

        if not collision_values:
            raise Exception("Expected collision values to exists")

        obj_x0, car_speed = collision_values
        obj_angle = object_angle_mapping[pair.obj_angle]

        if pair.obj_start_y == "left":
            obj_angle = -obj_angle
        elif pair.obj_start_y == "center":
            obj_angle = random.choice([obj_angle, -obj_angle])

        print(
            PedestrianTestConfiguration(
                pedestrian_appearance=pair.pedestrian_appearance,
                pedestrian_start_x=obj_x0,
                pedestrian_start_y=latteral_offset_mapping[pair.obj_start_y],
                pedestrian_angle=obj_angle,
                pedestrian_speed=object_speed_mapping[pair.obj_speed],
                car_speed=car_speed,
            )
        )


if __name__ == "__main__":
    generate_pedestrian_all_pairs()
    print()
    generate_object_all_pairs()
