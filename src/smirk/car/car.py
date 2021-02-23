from smirk.car.brakes import Brakes
from smirk.car.camera import Camera
from smirk.car.radar import Radar


class Car:
    def __init__(self, radar: Radar, camera: Camera, brakes: Brakes):
        self.radar = radar
        self.camera = camera
        self.brakes = brakes

    def get_radar_reading(self):
        return self.radar.get_latest_reading()

    def get_camera_frame(self):
        return self.camera.get_latest_frame()

    def brake(self):
        self.brakes.brake()
