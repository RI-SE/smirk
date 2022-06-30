#
# SMIRK
# Copyright (C) 2021-2022 RISE Research Institutes of Sweden AB
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
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
