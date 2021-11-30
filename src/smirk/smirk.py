import itertools
from typing import List

import numpy as np

from shared.radar_detection import RadarDetection
from smirk.pedestrian_detector.pedestrian_detector import (
    BoundingBox,
    PedestrianDetector,
)
from smirk.pedestrian_detector.ssd_hub_detector import SsdHubDetector
from smirk.safety_cage.noop_cage import NoopCage
from smirk.safety_cage.safety_cage import SafetyCage


class Smirk:
    TTC_THRESHOLD_SECONDS = 4
    HORIZONTAL_AOV = 45.5
    CAMERA_RADAR_DISTANCE = 1.8

    def __init__(
        self,
        pedestrian_detector: PedestrianDetector = None,
        safety_cage: SafetyCage = None,
    ):
        self.pedestrian_detector = pedestrian_detector or SsdHubDetector()
        self.safety_cage = safety_cage or NoopCage()

    def is_aeb(self, radar_detections: List[RadarDetection], camera_frame: np.ndarray):
        radar_detections_below_threshold = [
            detection
            for detection in radar_detections
            if detection.ttc < self.TTC_THRESHOLD_SECONDS
        ]

        if not radar_detections_below_threshold:
            return False

        pedestrian_detections = self.pedestrian_detector.detect_pedestrians(
            camera_frame
        )

        if not pedestrian_detections:
            return False

        radar_angles_distance_adjucted = [
            self.calculate_radar_angle_at_camera_position(detection)
            for detection in radar_detections_below_threshold
        ]

        bbox_angle_ranges = [
            self.approximate_angle_range_from_bbox(bbox)
            for bbox in pedestrian_detections
        ]

        for radar_angle, (bbox_min, bbox_max) in itertools.product(
            radar_angles_distance_adjucted, bbox_angle_ranges
        ):
            if bbox_min <= radar_angle <= bbox_max:
                return True

        return False

    def calculate_radar_angle_at_camera_position(self, detection: RadarDetection):
        return np.sign(detection.angle) * (
            90
            - np.rad2deg(
                np.arctan((detection.y + self.CAMERA_RADAR_DISTANCE) / abs(detection.x))
            )
        )

    def approximate_angle_range_from_bbox(
        self, bbox: BoundingBox, padding_fraction=0.1
    ):
        return (
            (np.array([bbox.x_min, bbox.x_max]) - 0.5)
            * self.HORIZONTAL_AOV
            * (1 + padding_fraction)
        )
