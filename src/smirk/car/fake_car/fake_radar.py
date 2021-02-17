from collections import deque
from typing import List

from smirk.car.radar import Radar
from smirk.car.radar_detection import RadarDetection

from .fake_sensor_exception import FakeSensorException


class FakeRadar(Radar):
    def __init__(self, reading_queue: List[RadarDetection]):
        self.reading_queue = deque(reading_queue)

    def get_latest_reading(self) -> List[RadarDetection]:
        if len(self.reading_queue):
            return [self.reading_queue.popleft()]
        else:
            raise FakeSensorException()
