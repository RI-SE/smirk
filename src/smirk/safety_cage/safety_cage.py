from abc import ABC, abstractmethod

import numpy as np


class SafetyCage(ABC):
    @abstractmethod
    def is_accepted(self, camera_frame: np.ndarray, predicted_box_crop: np.ndarray) -> bool:
        pass
