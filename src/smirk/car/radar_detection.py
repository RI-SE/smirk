from dataclasses import dataclass
from typing import Any, Union


@dataclass
class RadarDetection:
    reading: Any
    time_to_collision: Union[int, None]
