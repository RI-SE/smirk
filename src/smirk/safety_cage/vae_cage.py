import numpy as np
import tensorflow as tf

import config.paths
from smirk.safety_cage.safety_cage import SafetyCage


class VaeCage(SafetyCage):
    # TODO: Proper threshold + store/load somewhere else
    THRESHOLD = 2.6377532754582757e-04
    IMG_SIZE = [480, 752]

    def __init__(self) -> None:
        for gpu in tf.config.experimental.list_physical_devices("GPU"):
            tf.config.experimental.set_memory_growth(gpu, True)

        from alibi_detect.utils.saving import load_detector

        self.model = load_detector(config.paths.vae_model)
        self.model.threshold = self.THRESHOLD
        self.model.predict(np.random.random((1, *self.IMG_SIZE, 3)))

    def is_accepted(self, camera_frame: np.ndarray) -> bool:
        pred = self.model.predict(
            np.expand_dims(camera_frame / 255, 0),
            outlier_type="instance",
            batch_size=1,
            return_feature_score=False,
            return_instance_score=False,
        )

        is_outlier = bool(pred["data"]["is_outlier"][0])

        return not is_outlier