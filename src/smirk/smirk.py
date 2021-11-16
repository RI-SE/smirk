import numpy as np

from smirk.pedestrian_detector.pedestrian_detector import PedestrianDetector
from smirk.pedestrian_detector.ssd_hub_detector import SsdHubDetector
from smirk.safety_cage.noop_cage import NoopCage
from smirk.safety_cage.safety_cage import SafetyCage


class Smirk:
    TTC_THRESHOLD_SECONDS = 4

    def __init__(
        self,
        pedestrian_detector: PedestrianDetector = None,
        safety_cage: SafetyCage = None,
    ):
        self.pedestrian_detector = pedestrian_detector or SsdHubDetector()
        self.safety_cage = safety_cage or NoopCage()

    # TODO: Match detected bounding box with radar detection position
    def is_aeb(self, ttc: float, camera_frame: np.ndarray):

        return (
            ttc < self.TTC_THRESHOLD_SECONDS
            and self.pedestrian_detector.is_pedestrian(camera_frame)
            and self.safety_cage.is_accepted(camera_frame)
        )
