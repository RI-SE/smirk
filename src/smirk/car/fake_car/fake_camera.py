from collections import deque
from typing import List

import numpy as np
from PIL import Image

from smirk.car.camera import Camera

from .fake_sensor_exception import FakeSensorException


class FakeCamera(Camera):
    def __init__(self, img_paths: List[str]):
        self.reading_queue = deque(np.array(Image.open(path)) for path in img_paths)

    def get_latest_frame(self) -> np.ndarray:
        if len(self.reading_queue):
            return self.reading_queue.popleft()
        else:
            raise FakeSensorException()
