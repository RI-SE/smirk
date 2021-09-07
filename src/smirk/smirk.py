import numpy as np

from smirk.pedestrian_detector.pedestrian_detector import PedestrianDetector
from smirk.safety_cage.safety_cage import SafetyCage


class Smirk:
    TTC_THRESHOLD_SECONDS = 4

    def __init__(
        self, pedestrian_detector: PedestrianDetector, safety_cage: SafetyCage
    ):
        self.pedestrian_detector = pedestrian_detector
        self.safety_cage = safety_cage

    # TODO: Match detected bounding box with radar detection position
    def is_aeb(self, ttc: float, camera_frame: np.ndarray):

        return (
            ttc < self.TTC_THRESHOLD_SECONDS
            and self.pedestrian_detector.is_pedestrian(camera_frame)
            and self.safety_cage.is_accepted(camera_frame)
        )
