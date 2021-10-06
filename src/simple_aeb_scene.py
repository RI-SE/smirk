import math
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from simulators.prosivic.objects.camera import Camera
from simulators.prosivic.objects.car import Car
from simulators.prosivic.objects.distance_observer import DistanceObserver
from simulators.prosivic.objects.pedestrian import Pedestrian, PedestrianAppearance
from simulators.prosivic.objects.pedestrian_observer import PedestrianObserver
from simulators.prosivic.objects.position import Position
from simulators.prosivic.objects.radar import Radar
from simulators.prosivic.simulation import Simulation


@dataclass
class CollisionData:
    car_collision_position: Position
    pedestrian_collision_position: Position
    distance: float
    is_collision: bool
    has_car_passed_pedestrian: bool


@dataclass
class ScenarioSetup:
    pedestrian_appearance: PedestrianAppearance
    pedestrian_start_x: float
    pedestrian_start_y: float
    pedestrian_angle: float
    pedestrian_speed: float
    car_speed: float


class Direction(Enum):
    Left = "left"
    Right = "right"
    Forwards = "forwards"
    Backwards = "backwards"


class SimpleAebScene:
    SCRIPT_NAME = "simple_aeb.script"
    SAMPLE_RATE = 0.04
    EGO_CAR_NAME = "ego_car/car"
    PEDESTRIAN_NAME = "pedestrian/pedestrian"
    PEDESTRIAN_OBSERVER_NAME = "pedestrian_observer"
    CAR_WIDTH = 2
    CAR_LENGTH = 5
    CAMERA_NAME = "main_camera/cam"
    RADAR_NAME = "radar/radar"
    DISTANCE_OBSERVER_NAME = "collision_observer"
    ROAD_LEFT_Y = 2.8
    ROAD_RIGHT_Y = -2.8

    def __init__(self) -> None:
        self.simulation = Simulation(self.SCRIPT_NAME)
        self.car = Car(self.EGO_CAR_NAME, self.simulation)
        self.pedestrian_observer = PedestrianObserver(
            self.simulation, self.PEDESTRIAN_OBSERVER_NAME
        )
        self.camera = Camera(self.simulation, self.CAMERA_NAME)
        self.radar = Radar(self.RADAR_NAME, self.CAR_WIDTH)
        self.collision_observer = DistanceObserver(
            self.simulation, self.DISTANCE_OBSERVER_NAME
        )
        self.pedestrian: Optional[Pedestrian] = None
        self.current_setup: Optional[ScenarioSetup] = None

    def get_collision_data(self) -> CollisionData:
        distance_data = self.collision_observer.get_data()
        car_collision_position = distance_data.position_object1
        pedestrian_collision_position = distance_data.position_object2

        return CollisionData(
            car_collision_position=car_collision_position,
            pedestrian_collision_position=pedestrian_collision_position,
            distance=distance_data.distance,
            is_collision=self.is_collision(
                car_collision_position,
                pedestrian_collision_position,
                distance_data.distance,
            ),
            has_car_passed_pedestrian=self.has_car_passed_pedestrian(
                car_collision_position, pedestrian_collision_position
            ),
        )

    def is_collision(
        self,
        car_collision_position: Position,
        pedestrian_collision_position: Position,
        distance: float,
    ) -> bool:
        return (
            0 <= car_collision_position.x - pedestrian_collision_position.x <= 1
            and distance <= self.CAR_WIDTH / 2
        )

    def has_car_passed_pedestrian(
        self, car_collision_position: Position, pedestrian_collision_position: Position
    ) -> bool:
        return (
            car_collision_position.x - self.CAR_LENGTH > pedestrian_collision_position.x
        )

    def direction_from_angle(self, angle: float) -> Direction:
        rounded_angle = round(angle)

        if rounded_angle % 360 == 0:
            return Direction.Forwards
        if rounded_angle % 180 == 0:
            return Direction.Backwards
        if rounded_angle % 360 < 180:
            return Direction.Left

        return Direction.Right

    def has_pedestrian_crossed_road(self) -> bool:
        direction = self.direction_from_angle(
            self.pedestrian_observer.get_walkling_angle()
        )

        if direction == Direction.Left:
            return self.pedestrian_observer.get_position().y >= self.ROAD_LEFT_Y

        if direction == Direction.Right:
            return self.pedestrian_observer.get_position().y <= self.ROAD_RIGHT_Y

        return False

    def get_pedestrian_distance_walked(self) -> float:
        if self.current_setup is None:
            return 0

        current_position = self.pedestrian_observer.get_position()
        start_x = self.current_setup.pedestrian_start_x
        start_y = self.current_setup.pedestrian_start_y

        return math.hypot(
            (current_position.x - start_x), (current_position.y - start_y)
        )

    def _step_until_dds_init(self) -> None:
        """Step simulation until all DDS data samples are available."""
        # Radar has lowest sample rate.
        prev_timestamp = self.radar.get_detections().timestamp
        while True:
            self.simulation.step(1)
            current_timestamp = self.radar.get_detections().timestamp

            if not prev_timestamp == current_timestamp:
                return

            prev_timestamp = current_timestamp

    def reset_scene(self):
        if self.current_setup:
            self.simulation.stop()
            self.current_setup = None

        if self.pedestrian:
            self.pedestrian.delete()
            self.pedestrian = None

    def setup_scenario(
        self,
        pedestrian_appearance: PedestrianAppearance,
        pedestrian_start_x: float,
        pedestrian_start_y: float,
        pedestrian_angle: float,
        pedestrian_speed: float,
        car_speed: float,
    ) -> None:
        self.reset_scene()

        self.current_setup = ScenarioSetup(
            pedestrian_appearance,
            pedestrian_start_x,
            pedestrian_start_y,
            pedestrian_angle,
            pedestrian_speed,
            car_speed,
        )

        self.pedestrian = Pedestrian(self.simulation, pedestrian_appearance)
        self.pedestrian_observer.set_pedestrian(self.pedestrian.name)
        self.collision_observer.set_object2(self.pedestrian.name)
        for mesh in self.pedestrian.get_mesh_names():
            self.camera.add_mesh_to_labeling(mesh)

        self.simulation.pause()

        self.pedestrian.set_angle(pedestrian_angle)
        self.pedestrian.set_position(pedestrian_start_x, pedestrian_start_y)
        self.pedestrian.set_speed(pedestrian_speed)

        self.car.set_init_speed(car_speed)
        self.car.set_cruise_control(car_speed)

        self._step_until_dds_init()

    def setup_scenario_walk_from_left(
        self,
        pedestrian_appearance: PedestrianAppearance,
        pedestrian_distance_from_car: float,
        pedestrian_distance_from_road: float,
        pedestrian_walking_angle: float,
        pedestrian_walking_speed: float,
        car_speed: float,
    ) -> None:
        transformed_angle = -pedestrian_walking_angle

        self.setup_scenario(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=pedestrian_distance_from_car,
            pedestrian_start_y=self.ROAD_LEFT_Y + pedestrian_distance_from_road,
            pedestrian_angle=transformed_angle,
            pedestrian_speed=pedestrian_walking_speed,
            car_speed=car_speed,
        )

    def setup_scenario_walk_from_right(
        self,
        pedestrian_appearance: PedestrianAppearance,
        pedestrian_distance_from_car: float,
        pedestrian_distance_from_road: float,
        pedestrian_walking_angle: float,
        pedestrian_walking_speed: float,
        car_speed: float,
    ) -> None:
        self.setup_scenario(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=pedestrian_distance_from_car,
            pedestrian_start_y=self.ROAD_RIGHT_Y - pedestrian_distance_from_road,
            pedestrian_angle=pedestrian_walking_angle,
            pedestrian_speed=pedestrian_walking_speed,
            car_speed=car_speed,
        )

    def setup_scenario_walk_away(
        self,
        pedestrian_appearance: PedestrianAppearance,
        pedestrian_distance_from_car: float,
        pedestrian_offset_from_road_center: float,
        pedestrian_walking_speed: float,
        car_speed: float,
    ) -> None:
        self.setup_scenario(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=pedestrian_distance_from_car,
            pedestrian_start_y=pedestrian_offset_from_road_center,
            pedestrian_angle=0,
            pedestrian_speed=pedestrian_walking_speed,
            car_speed=car_speed,
        )

    def setup_scenario_walk_towards(
        self,
        pedestrian_appearance: PedestrianAppearance,
        pedestrian_distance_from_car: float,
        pedestrian_offset_from_road_center: float,
        pedestrian_walking_speed: float,
        car_speed: float,
    ) -> None:
        self.setup_scenario(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=pedestrian_distance_from_car,
            pedestrian_start_y=pedestrian_offset_from_road_center,
            pedestrian_angle=180,
            pedestrian_speed=pedestrian_walking_speed,
            car_speed=car_speed,
        )
