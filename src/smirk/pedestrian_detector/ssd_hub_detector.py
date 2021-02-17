import logging
from typing import Any, Dict

import numpy as np
import tensorflow_hub as hub

from smirk.pedestrian_detector.pedestrian_detector import PedestrianDetector


class SsdHubDetector(PedestrianDetector):
    PERSON_CLASS_ID = 1
    DETECTION_THRESHOLD = 0.5

    def __init__(self, debug_fn=None):
        self.debug_fn = debug_fn

        logging.info("Loading SSD from tensorflow hub.")
        self.model: Any = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")
        logging.info("Model loaded.")
        logging.info("Model warmup.")
        self.model(np.zeros((1, 300, 300, 3)))
        logging.info("Model ready.")

    def is_pedestrian(self, camera_frame: np.ndarray) -> bool:
        detections: Dict = self.model(np.expand_dims(camera_frame, axis=0))
        person_mask = detections["detection_classes"] == self.PERSON_CLASS_ID
        person_scores: np.ndarray = detections["detection_scores"][person_mask]

        if self.debug_fn:
            self.debug_fn(camera_frame, detections)

        return np.any(person_scores > self.DETECTION_THRESHOLD)
