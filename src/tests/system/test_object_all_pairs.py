import argparse

from tests.system.system_test_runner import ObjectTestConfiguration, SystemTestRunner

object_all_pairs = [
    ObjectTestConfiguration(
        object_type="box",
        start_x=15,
        start_y=5,
        end_x=15,
        end_y=-5,
        angle=-90,
        speed=1,
        car_speed=3.33,
    ),
    ObjectTestConfiguration(
        object_type="box",
        start_x=25,
        start_y=5,
        end_x=25,
        end_y=-5,
        angle=-90,
        speed=3,
        car_speed=13.64,
    ),
    ObjectTestConfiguration(
        object_type="box",
        start_x=50,
        start_y=-5,
        end_x=50,
        end_y=5,
        angle=90,
        speed=1,
        car_speed=9,
    ),
    ObjectTestConfiguration(
        object_type="cone",
        start_x=22,
        start_y=5,
        end_x=22,
        end_y=-5,
        angle=-90,
        speed=1,
        car_speed=4,
    ),
    ObjectTestConfiguration(
        object_type="cone",
        start_x=25,
        start_y=-5,
        end_x=25,
        end_y=5,
        angle=90,
        speed=3,
        car_speed=15,
    ),
    ObjectTestConfiguration(
        object_type="cone",
        start_x=29,
        start_y=5,
        end_x=29,
        end_y=-5,
        angle=-90,
        speed=1,
        car_speed=5.27,
    ),
    ObjectTestConfiguration(
        object_type="cone",
        start_x=80,
        start_y=5,
        end_x=80,
        end_y=-5,
        angle=-90,
        speed=1,
        car_speed=17.78,
    ),
    ObjectTestConfiguration(
        object_type="pyramid",
        start_x=15,
        start_y=5,
        end_x=15,
        end_y=-5,
        angle=-90,
        speed=1,
        car_speed=3.33,
    ),
    ObjectTestConfiguration(
        object_type="pyramid",
        start_x=25,
        start_y=5,
        end_x=25,
        end_y=-5,
        angle=-90,
        speed=3,
        car_speed=15,
    ),
    ObjectTestConfiguration(
        object_type="pyramid",
        start_x=93,
        start_y=-5,
        end_x=93,
        end_y=5,
        angle=90,
        speed=1,
        car_speed=16.91,
    ),
    ObjectTestConfiguration(
        object_type="sphere",
        start_x=10,
        start_y=-5,
        end_x=10,
        end_y=5,
        angle=90,
        speed=3,
        car_speed=6.67,
    ),
    ObjectTestConfiguration(
        object_type="sphere",
        start_x=29,
        start_y=5,
        end_x=29,
        end_y=-5,
        angle=-90,
        speed=3,
        car_speed=17.4,
    ),
    ObjectTestConfiguration(
        object_type="sphere",
        start_x=72,
        start_y=5,
        end_x=72,
        end_y=-5,
        angle=-90,
        speed=1,
        car_speed=14.4,
    ),
]


def test_object_all_pairs(add_noise: bool = False):
    runner = SystemTestRunner()
    runner.run_all(object_all_pairs, add_noise)
    runner.results_to_csv()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--noisy",
        help="Randomly add jitter in the range from -10% to +10% to all numerical values.",
        action="store_true",
    )
    args = parser.parse_args()

    test_object_all_pairs(args.noisy)
