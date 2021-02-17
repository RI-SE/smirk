from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Union


@dataclass
class RadarDetection:
    reading: Any
    time_to_collision: Union[int, None]


class Radar(ABC):
    @abstractmethod
    def get_latest_reading(self) -> List[RadarDetection]:
        pass
