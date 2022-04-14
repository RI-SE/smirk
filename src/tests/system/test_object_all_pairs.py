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
        scenario_id="TC-26",
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
        scenario_id="TC-27",
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
        scenario_id="TC-28",
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
        scenario_id="TC-29",
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
        scenario_id="TC-30",
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
        scenario_id="TC-31",
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
        scenario_id="TC-32",
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
        scenario_id="TC-33",
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
        scenario_id="TC-34",
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
        scenario_id="TC-35",
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
        scenario_id="TC-36",
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
        scenario_id="TC-37",
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
        scenario_id="TC-38",
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
        help="Randomly add jitter in the range from -10%% to +10%% to all numerical values.",
        action="store_true",
    )
    args = parser.parse_args()

    test_object_all_pairs(args.noisy)
