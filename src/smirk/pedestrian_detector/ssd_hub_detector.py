import logging
from typing import Any, Dict, List

import numpy as np
import tensorflow_hub as hub

from smirk.pedestrian_detector.pedestrian_detector import (
    BoundingBox,
    PedestrianDetector,
)


class SsdHubDetector(PedestrianDetector):
    PEDESTRIAN_CLASS_ID = 1
    DETECTION_THRESHOLD = 0.5

    def __init__(self):
        logging.info("Loading SSD from tensorflow hub.")
        self.model: Any = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")
        logging.info("Model loaded.")
        logging.info("Model warmup.")
        self.model(np.zeros((1, 300, 300, 3)))
        logging.info("Model ready.")

    def detect_pedestrians(self, camera_frame: np.ndarray) -> List[BoundingBox]:
        detections: Dict = self.model(np.expand_dims(camera_frame, axis=0))
        pedestrian_boxes_above_threshold = detections["detection_boxes"][
            (detections["detection_classes"] == self.PEDESTRIAN_CLASS_ID)
            & (detections["detection_scores"] > self.DETECTION_THRESHOLD)
        ].numpy()

        return [
            self.detection_boxes_to_bounding_box(detection)
            for detection in pedestrian_boxes_above_threshold
        ]

    def detection_boxes_to_bounding_box(self, detection: List[float]) -> BoundingBox:
        y_min, x_min, y_max, x_max = detection

        return BoundingBox(x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max)
