import numpy as np

from smirk.safety_cage.safety_cage import SafetyCage


class NoopCage(SafetyCage):
    def is_accepted(
        self, camera_frame: np.ndarray, predicted_box_crop: np.ndarray
    ) -> bool:
        return True
