from abc import ABC, abstractmethod
from typing import List

from .radar_detection import RadarDetection


class Radar(ABC):
    @abstractmethod
    def get_latest_reading(self) -> List[RadarDetection]:
        pass
