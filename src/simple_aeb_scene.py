import math
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from simulators.prosivic.objects.camera import Camera
from simulators.prosivic.objects.car import Car
from simulators.prosivic.objects.distance_observer import DistanceObserver
from simulators.prosivic.objects.object_observer import ObjectObserver
from simulators.prosivic.objects.pedestrian import Pedestrian, PedestrianAppearance
from simulators.prosivic.objects.pedestrian_observer import PedestrianObserver
from simulators.prosivic.objects.position import Position
from simulators.prosivic.objects.position_interpolator import PositionInterpolator
from simulators.prosivic.objects.radar import Radar
from simulators.prosivic.objects.simple_object import SimpleObject, SimpleObjectType
from simulators.prosivic.simulation import Simulation


@dataclass
class CollisionData:
    car_collision_position: Position
    object_collision_position: Position
    distance: float
    is_collision: bool
    has_car_passed_object: bool


@dataclass
class ScenarioSetup:
    object_type: str
    start_x: float
    start_y: float
    object_angle: float
    object_speed: float
    car_speed: float


class Direction(Enum):
    Left = "left"
    Right = "right"
    Forwards = "forwards"
    Backwards = "backwards"


class SimpleAebScene:
    SCRIPT_NAME = "simple_aeb.script"
    EGO_CAR_NAME = "ego_car/car"
    CAR_WIDTH = 2
    CAR_LENGTH = 5
    CAMERA_NAME = "main_camera/cam"
    RADAR_NAME = "radar/radar"
    DISTANCE_OBSERVER_NAME = "collision_observer"
    ROAD_LEFT_Y = 2.8
    ROAD_RIGHT_Y = -2.8

    def __init__(self) -> None:
        self.simulation = Simulation(self.SCRIPT_NAME)
        self.car = Car(self.simulation, self.EGO_CAR_NAME)
        self.camera = Camera(self.simulation, self.CAMERA_NAME)
        self.radar = Radar(self.RADAR_NAME, self.CAR_WIDTH / 2)
        self.collision_observer = DistanceObserver(
            self.simulation, self.DISTANCE_OBSERVER_NAME
        )
        self.object_observer: Optional[Union[PedestrianObserver, ObjectObserver]] = None
        self.crossing_object: Optional[Union[Pedestrian, SimpleObject]] = None
        self.position_interpolator: Optional[PositionInterpolator] = None
        self.current_setup: Optional[ScenarioSetup] = None

    def get_collision_data(self) -> CollisionData:
        distance_data = self.collision_observer.get_data()
        car_collision_position = distance_data.position_object1
        object_collision_position = distance_data.position_object2

        return CollisionData(
            car_collision_position=car_collision_position,
            object_collision_position=object_collision_position,
            distance=distance_data.distance,
            is_collision=self.is_collision(
                car_collision_position,
                object_collision_position,
                distance_data.distance,
            ),
            has_car_passed_object=self.has_car_passed_object(
                car_collision_position, object_collision_position
            ),
        )

    def is_collision(
        self,
        car_collision_position: Position,
        object_collision_position: Position,
        distance: float,
    ) -> bool:
        return (
            0 <= car_collision_position.x - object_collision_position.x <= 1
            and distance <= self.CAR_WIDTH / 2
        )

    def has_car_passed_object(
        self, car_collision_position: Position, object_collision_position: Position
    ) -> bool:
        return car_collision_position.x - self.CAR_LENGTH > object_collision_position.x

    def direction_from_angle(self, angle: float) -> Direction:
        rounded_angle = round(angle)

        if rounded_angle % 360 == 0:
            return Direction.Forwards
        if rounded_angle % 180 == 0:
            return Direction.Backwards
        if rounded_angle % 360 < 180:
            return Direction.Left

        return Direction.Right

    def has_object_crossed_road(self) -> bool:
        if not self.current_setup or not self.object_observer:
            raise Exception("No scenario initialized")

        direction = self.direction_from_angle(self.current_setup.object_angle)

        if direction == Direction.Left:
            return self.object_observer.get_position().y >= self.ROAD_LEFT_Y

        if direction == Direction.Right:
            return self.object_observer.get_position().y <= self.ROAD_RIGHT_Y

        return False

    def get_object_distance_traveled(self) -> float:
        if not self.current_setup or not self.object_observer:
            raise Exception("No scenario initialized")

        current_position = self.object_observer.get_position()
        start_x = self.current_setup.start_x
        start_y = self.current_setup.start_y

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

        if self.crossing_object:
            self.crossing_object.delete()
            self.crossing_object = None

        if self.object_observer:
            self.object_observer.delete()
            self.object_observer = None

        if self.position_interpolator:
            self.position_interpolator.delete()
            self.position_interpolator = None

    def setup_pedestrian_scenario(
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

        self.crossing_object = Pedestrian(self.simulation, pedestrian_appearance)

        self.object_observer = PedestrianObserver(self.simulation)
        self.object_observer.set_object(self.crossing_object.name)

        self.collision_observer.set_object2(self.crossing_object.name)

        for mesh in self.crossing_object.get_mesh_names():
            self.camera.add_mesh_to_labeling(mesh)

        self.simulation.pause()

        self.crossing_object.set_angle(pedestrian_angle)
        self.crossing_object.set_position(pedestrian_start_x, pedestrian_start_y)
        self.crossing_object.set_speed(pedestrian_speed)

        self.car.set_init_speed(car_speed)
        self.car.set_cruise_control(car_speed)

        self._step_until_dds_init()

    def setup_scenario_pedestrian_from_left(
        self,
        pedestrian_appearance: PedestrianAppearance,
        pedestrian_distance_from_car: float,
        pedestrian_distance_from_road: float,
        pedestrian_walking_angle: float,
        pedestrian_walking_speed: float,
        car_speed: float,
    ) -> None:
        transformed_angle = -pedestrian_walking_angle

        self.setup_pedestrian_scenario(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=pedestrian_distance_from_car,
            pedestrian_start_y=self.ROAD_LEFT_Y + pedestrian_distance_from_road,
            pedestrian_angle=transformed_angle,
            pedestrian_speed=pedestrian_walking_speed,
            car_speed=car_speed,
        )

    def setup_scenario_pedestrian_from_right(
        self,
        pedestrian_appearance: PedestrianAppearance,
        pedestrian_distance_from_car: float,
        pedestrian_distance_from_road: float,
        pedestrian_walking_angle: float,
        pedestrian_walking_speed: float,
        car_speed: float,
    ) -> None:
        self.setup_pedestrian_scenario(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=pedestrian_distance_from_car,
            pedestrian_start_y=self.ROAD_RIGHT_Y - pedestrian_distance_from_road,
            pedestrian_angle=pedestrian_walking_angle,
            pedestrian_speed=pedestrian_walking_speed,
            car_speed=car_speed,
        )

    def setup_scenario_pedestrian_away(
        self,
        pedestrian_appearance: PedestrianAppearance,
        pedestrian_distance_from_car: float,
        pedestrian_offset_from_road_center: float,
        pedestrian_walking_speed: float,
        car_speed: float,
    ) -> None:
        self.setup_pedestrian_scenario(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=pedestrian_distance_from_car,
            pedestrian_start_y=pedestrian_offset_from_road_center,
            pedestrian_angle=0,
            pedestrian_speed=pedestrian_walking_speed,
            car_speed=car_speed,
        )

    def setup_scenario_pedestrian_towards(
        self,
        pedestrian_appearance: PedestrianAppearance,
        pedestrian_distance_from_car: float,
        pedestrian_offset_from_road_center: float,
        pedestrian_walking_speed: float,
        car_speed: float,
    ) -> None:
        self.setup_pedestrian_scenario(
            pedestrian_appearance=pedestrian_appearance,
            pedestrian_start_x=pedestrian_distance_from_car,
            pedestrian_start_y=pedestrian_offset_from_road_center,
            pedestrian_angle=180,
            pedestrian_speed=pedestrian_walking_speed,
            car_speed=car_speed,
        )

    def setup_object_scenario(
        self,
        object_type: SimpleObjectType,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        angle: float,
        speed: float,
        car_speed: float,
    ):
        self.reset_scene()

        self.current_setup = ScenarioSetup(
            object_type,
            start_x,
            start_y,
            angle,
            speed,
            car_speed,
        )

        self.crossing_object = SimpleObject(self.simulation, object_type)

        self.object_observer = ObjectObserver(self.simulation)
        self.object_observer.set_object(self.crossing_object.name)

        self.collision_observer.set_object2(self.crossing_object.name)

        self.position_interpolator = PositionInterpolator(self.simulation)
        self.position_interpolator.set_controlled_object(self.crossing_object.name)
        self.position_interpolator.add_key_frame(x=start_x, y=start_y, rotation_z=angle)
        self.position_interpolator.add_key_frame(x=end_x, y=end_y, rotation_z=angle)
        self.position_interpolator.set_seconds_between_frames(
            math.hypot((end_x - start_x), (end_y - start_y)) / speed
        )
        self.position_interpolator.play()

        self.car.set_init_speed(car_speed)
        self.car.set_cruise_control(car_speed)

        self.simulation.pause()
        self._step_until_dds_init()

    def setup_scenario_object_from_left(
        self,
        object_type: SimpleObjectType,
        distance_from_car: float,
        distance_from_road: float,
        speed: float,
        car_speed: float,
    ) -> None:
        self.setup_object_scenario(
            object_type=object_type,
            start_x=distance_from_car,
            start_y=self.ROAD_LEFT_Y + distance_from_road,
            end_x=distance_from_car,
            end_y=self.ROAD_RIGHT_Y - distance_from_road,
            angle=-90,
            speed=speed,
            car_speed=car_speed,
        )

    def setup_scenario_object_from_right(
        self,
        object_type: SimpleObjectType,
        distance_from_car: float,
        distance_from_road: float,
        speed: float,
        car_speed: float,
    ) -> None:
        self.setup_object_scenario(
            object_type=object_type,
            start_x=distance_from_car,
            start_y=self.ROAD_RIGHT_Y - distance_from_road,
            end_x=distance_from_car,
            end_y=self.ROAD_LEFT_Y + distance_from_road,
            angle=90,
            speed=speed,
            car_speed=car_speed,
        )
