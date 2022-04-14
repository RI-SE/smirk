from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class BoundingBox:
    x_min: int
    y_min: int
    x_max: int
    y_max: int


class PedestrianDetector(ABC):
    @abstractmethod
    def detect_pedestrians(self, camera_frame: np.ndarray) -> List[BoundingBox]:
        pass
