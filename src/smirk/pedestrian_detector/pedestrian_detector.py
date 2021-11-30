from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class BoundingBox:
    x_min: float
    x_max: float
    y_min: float
    y_max: float


class PedestrianDetector(ABC):
    @abstractmethod
    def detect_pedestrians(self, camera_frame: np.ndarray) -> List[BoundingBox]:
        pass
