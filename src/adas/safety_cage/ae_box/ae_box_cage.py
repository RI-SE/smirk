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
from typing import Any, Dict, cast

import numpy as np
import tensorflow as tf

import config.paths
from adas.safety_cage.safety_cage import SafetyCage
from yolov5.utils.augmentations import letterbox


class AeBoxCage(SafetyCage):
    # TODO: Proper threshold + store/load somewhere else
    THRESHOLD = 4e-3
    IMG_SIZE = [160, 64]

    def __init__(self) -> None:
        for gpu in tf.config.experimental.list_physical_devices("GPU"):
            tf.config.experimental.set_memory_growth(gpu, True)

        from alibi_detect.od.ae import OutlierAE
        from alibi_detect.utils.saving import load_detector

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
