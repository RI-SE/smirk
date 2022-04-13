from typing import Any, Dict, cast
import numpy as np
import tensorflow as tf

import config.paths
from smirk.safety_cage.safety_cage import SafetyCage
from yolov5.utils.augmentations import letterbox


class AeBoxCage(SafetyCage):
    # TODO: Proper threshold + store/load somewhere else
    THRESHOLD = 4e-3
    IMG_SIZE = [160, 64]

    def __init__(self) -> None:
        for gpu in tf.config.experimental.list_physical_devices("GPU"):
            tf.config.experimental.set_memory_growth(gpu, True)

        from alibi_detect.utils.saving import load_detector
        from alibi_detect.od.ae import OutlierAE

        self.model = cast(OutlierAE, load_detector(config.paths.ae_box_model))
        self.model.threshold = self.THRESHOLD
        self.model.predict(np.random.random((1, *self.IMG_SIZE, 3)).astype(np.float32))

    def is_accepted(
        self, camera_frame: np.ndarray, predicted_box_crop: np.ndarray, distance: float
    ) -> bool:
        if distance <= 10:
            return True
        resized_box, *_ = letterbox(
            predicted_box_crop, self.IMG_SIZE, auto=False, scaleFill=True
        )
        pred: Dict[Any, Any] = self.model.predict(
            np.expand_dims(resized_box / 255, 0).astype(np.float32),
            outlier_type="instance",
            return_feature_score=False,
            return_instance_score=False,
        )

        is_outlier = bool(pred["data"]["is_outlier"][0])

        return not is_outlier
