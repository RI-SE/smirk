#
# SMIRK
# Copyright (C) 2021-2022 RISE Research Institutes of Sweden AB
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import itertools
from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from shared.radar_detection import RadarDetection
from smirk.pedestrian_detector.pedestrian_detector import BoundingBox
from smirk.pedestrian_detector.yolo.yolo_detector import YoloDetector
from smirk.safety_cage.ae_box.ae_box_cage import AeBoxCage


@dataclass
class SmirkResult:
    brake: bool = False
    radar: bool = False
    camera: Optional[bool] = None
    radar_camera_fusion: Optional[bool] = None
    bbox: Optional[BoundingBox] = None
    bbox_img: Optional[np.ndarray] = None
    cage: Optional[bool] = None


class Smirk:
    def __init__(
        self,
        ttc_threshold_seconds=4,
        camera_radar_distance=1.8,
        horizontal_aov=45.5,
        img_width=752,
        img_height=480,
    ):
        self.safety_cage = AeBoxCage()
        self.pedestrian_detector = YoloDetector()

        self.ttc_threshold_seconds = ttc_threshold_seconds
        self.camera_radar_distance = camera_radar_distance
        self.horizontal_aov = horizontal_aov
        self.img_width = img_width
        self.img_height = img_height

    def is_aeb(
        self, radar_detections: List[RadarDetection], camera_frame: np.ndarray
    ) -> SmirkResult:
        result = SmirkResult()

        radar_detections_below_threshold = self.filter_detections_below_threshold(
            radar_detections
        )
        result.radar = bool(radar_detections_below_threshold)
        if not radar_detections_below_threshold:
            return result

        pedestrian_detections = self.pedestrian_detector.detect_pedestrians(
            camera_frame
        )
        result.camera = bool(pedestrian_detections)
        if not pedestrian_detections:
            return result

        for radar_detection, pedestrian_detection in itertools.product(
            radar_detections_below_threshold, pedestrian_detections
        ):
            result.radar_camera_fusion = self.radar_camera_fusion(
                radar_detection, pedestrian_detection
            )
            if result.radar_camera_fusion:
                result.bbox = pedestrian_detection
                result.bbox_img = self.crop_bounding_box(
                    camera_frame, pedestrian_detection
                )
                result.cage = self.safety_cage.is_accepted(
                    camera_frame, result.bbox_img, radar_detection.distance
                )

                if result.cage:
                    result.brake = True
                    return result

        return result

    def filter_detections_below_threshold(self, radar_detections: List[RadarDetection]):
        return [
            detection
            for detection in radar_detections
            if detection.ttc < self.ttc_threshold_seconds
        ]

    def radar_camera_fusion(
        self, radar_detection: RadarDetection, pedestrian_detection: BoundingBox
    ):
        radar_angle = self.calculate_radar_angle_at_camera_position(radar_detection)
        bbox_min_angle, bbox_max_angle = self.approximate_angle_range_from_bbox(
            pedestrian_detection
        )

        return bbox_min_angle <= radar_angle <= bbox_max_angle

    def crop_bounding_box(self, camera_frame: np.ndarray, bbox: BoundingBox):
        return camera_frame[bbox.y_min : bbox.y_max, bbox.x_min : bbox.x_max, :]

    def calculate_radar_angle_at_camera_position(self, detection: RadarDetection):
        return np.sign(detection.angle) * (
            90
            - np.rad2deg(
                np.arctan((detection.y + self.camera_radar_distance) / abs(detection.x))
            )
        )

    def approximate_angle_range_from_bbox(
        self, bbox: BoundingBox, padding_fraction=0.1
    ) -> np.ndarray:
        bbox_x = np.array([bbox.x_min, bbox.x_max])
        bbox_x = bbox_x / self.img_width  # Normalize
        bbox_x = bbox_x - 0.5  # Relative center

        return bbox_x * self.horizontal_aov * (1 + padding_fraction)
