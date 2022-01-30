from typing import List

import numpy as np

from smirk.pedestrian_detector.pedestrian_detector import (
    BoundingBox,
    PedestrianDetector,
)


class NoopDetector(PedestrianDetector):
    def detect_pedestrians(self, camera_frame: np.ndarray) -> List[BoundingBox]:
        return []
