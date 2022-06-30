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
from typing import List

import numpy as np

from smirk.adas.pedestrian_detector.pedestrian_detector import (
    BoundingBox,
    PedestrianDetector,
)


class NoopDetector(PedestrianDetector):
    def detect_pedestrians(self, camera_frame: np.ndarray) -> List[BoundingBox]:
        return []
