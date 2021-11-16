from tests.system.system_test_runner import SystemTestConfiguration, SystemTestRunner

all_pairs = [
    SystemTestConfiguration(
        pedestrian_appearance="child",
        pedestrian_start_x=21.5,
        pedestrian_start_y=5,
        pedestrian_angle=-45,
        pedestrian_speed=1,
        car_speed=3.47,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="child",
        pedestrian_start_x=26,
        pedestrian_start_y=5,
        pedestrian_angle=-90,
        pedestrian_speed=1,
        car_speed=5.78,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="child",
        pedestrian_start_x=38,
        pedestrian_start_y=0,
        pedestrian_angle=0,
        pedestrian_speed=0,
        car_speed=14,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="child",
        pedestrian_start_x=54.5,
        pedestrian_start_y=-5,
        pedestrian_angle=135,
        pedestrian_speed=3,
        car_speed=18.9,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="female_business",
        pedestrian_start_x=20,
        pedestrian_start_y=0,
        pedestrian_angle=180,
        pedestrian_speed=3,
        car_speed=16,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="female_business",
        pedestrian_start_x=23.5,
        pedestrian_start_y=5,
        pedestrian_angle=-45,
        pedestrian_speed=1,
        car_speed=3.73,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="female_business",
        pedestrian_start_x=46,
        pedestrian_start_y=5,
        pedestrian_angle=-135,
        pedestrian_speed=1,
        car_speed=5.8,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="female_business",
        pedestrian_start_x=50,
        pedestrian_start_y=-5,
        pedestrian_angle=90,
        pedestrian_speed=1,
        car_speed=10,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="female_casual",
        pedestrian_start_x=15,
        pedestrian_start_y=0,
        pedestrian_angle=135,
        pedestrian_speed=0,
        car_speed=11,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="female_casual",
        pedestrian_start_x=24.5,
        pedestrian_start_y=-5,
        pedestrian_angle=135,
        pedestrian_speed=1,
        car_speed=3.14,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="female_casual",
        pedestrian_start_x=45,
        pedestrian_start_y=5,
        pedestrian_angle=-135,
        pedestrian_speed=1,
        car_speed=5.66,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="female_casual",
        pedestrian_start_x=46,
        pedestrian_start_y=5,
        pedestrian_angle=-90,
        pedestrian_speed=1,
        car_speed=10.22,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="female_casual",
        pedestrian_start_x=50.5,
        pedestrian_start_y=6,
        pedestrian_angle=-45,
        pedestrian_speed=3,
        car_speed=18.6,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="male_business",
        pedestrian_start_x=21,
        pedestrian_start_y=-5,
        pedestrian_angle=45,
        pedestrian_speed=1,
        car_speed=3.68,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="male_business",
        pedestrian_start_x=25,
        pedestrian_start_y=5,
        pedestrian_angle=-90,
        pedestrian_speed=3,
        car_speed=15,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="male_business",
        pedestrian_start_x=26.5,
        pedestrian_start_y=5,
        pedestrian_angle=-135,
        pedestrian_speed=1,
        car_speed=3.46,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="male_business",
        pedestrian_start_x=54,
        pedestrian_start_y=0,
        pedestrian_angle=0,
        pedestrian_speed=1,
        car_speed=9,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="male_casual",
        pedestrian_start_x=34,
        pedestrian_start_y=-5,
        pedestrian_angle=45,
        pedestrian_speed=1,
        car_speed=5.52,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="male_casual",
        pedestrian_start_x=34.5,
        pedestrian_start_y=5,
        pedestrian_angle=-135,
        pedestrian_speed=1,
        car_speed=4.71,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="male_casual",
        pedestrian_start_x=47.5,
        pedestrian_start_y=4,
        pedestrian_angle=-45,
        pedestrian_speed=1,
        car_speed=10.3,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="male_casual",
        pedestrian_start_x=74,
        pedestrian_start_y=0,
        pedestrian_angle=90,
        pedestrian_speed=0,
        car_speed=19,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="male_worker",
        pedestrian_start_x=10,
        pedestrian_start_y=5,
        pedestrian_angle=-90,
        pedestrian_speed=3,
        car_speed=6,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="male_worker",
        pedestrian_start_x=17.5,
        pedestrian_start_y=-5,
        pedestrian_angle=45,
        pedestrian_speed=1,
        car_speed=3.46,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="male_worker",
        pedestrian_start_x=39,
        pedestrian_start_y=5,
        pedestrian_angle=-135,
        pedestrian_speed=1,
        car_speed=4.81,
    ),
    SystemTestConfiguration(
        pedestrian_appearance="male_worker",
        pedestrian_start_x=86.5,
        pedestrian_start_y=5,
        pedestrian_angle=-135,
        pedestrian_speed=1,
        car_speed=12.89,
    ),
]


def test_all_pairs(result_path=None):
    runner = SystemTestRunner()
    runner.run_all(all_pairs)
    runner.results_to_csv(result_path)


if __name__ == "__main__":
    test_all_pairs()
