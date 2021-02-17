from abc import ABC, abstractmethod

import numpy as np


class PedestrianDetector(ABC):
    @abstractmethod
    def is_pedestrian(self, camera_frame: np.ndarray) -> bool:
        pass
