import numpy as np

from smirk.pedestrian_detector.pedestrian_detector import PedestrianDetector


class NoopDetector(PedestrianDetector):
    def is_pedestrian(self, camera_frame: np.ndarray) -> bool:
        return False
