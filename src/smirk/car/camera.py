from abc import ABC, abstractmethod

import numpy as np


class Camera(ABC):
    @abstractmethod
    def get_latest_frame(self) -> np.ndarray:
        pass
