from typing import List

import numpy as np
import torch

import config.paths
from smirk.pedestrian_detector.pedestrian_detector import (
    BoundingBox,
    PedestrianDetector,
)


class YoloDetector(PedestrianDetector):
    DETECTION_THRESHOLD = 0.5

    def __init__(self):
        # TODO: use local yolov5 project
        self.model = torch.hub.load(
            "ultralytics/yolov5", "custom", path=config.paths.yolo_model.absolute()
        )

        self.model.conf = self.DETECTION_THRESHOLD

    def detect_pedestrians(self, camera_frame: np.ndarray) -> List[BoundingBox]:
        detections = self.model(camera_frame).xyxyn[0].cpu().numpy()

        return [self.detection_to_bounding_box(detection) for detection in detections]

    def detection_to_bounding_box(self, detection: List[float]) -> BoundingBox:
        # Detection: [x_min, y_min, x_max, y_max, conf, cls]
        x_min, y_min, x_max, y_max, *_ = detection

        return BoundingBox(x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max)
