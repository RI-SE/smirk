import logging
from typing import Any, Dict, List

import numpy as np
import tensorflow_hub as hub

from smirk.pedestrian_detector.pedestrian_detector import (
    BoundingBox,
    PedestrianDetector,
)


class SsdHubDetector(PedestrianDetector):
    PERSON_CLASS_ID = 1
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
        person_mask = detections["detection_classes"] == self.PERSON_CLASS_ID
        person_scores: np.ndarray = detections["detection_scores"][person_mask]

        return [
            BoundingBox(x_min.numpy(), x_max.numpy(), y_min.numpy(), y_max.numpy())
            for y_min, x_min, y_max, x_max in detections["detection_boxes"][
                person_mask
            ][person_scores > self.DETECTION_THRESHOLD]
        ]
