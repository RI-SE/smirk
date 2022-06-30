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
from dataclasses import dataclass
from typing import Any

import numpy as np

from smirk.simulators.prosivic.simulation import Simulation

from ..psvdds import psvdds


@dataclass
class CameraFrame:
    """A camera frame

    Attributes:
        timestamp: Prosivic timestamp in microseconds.
        frame_data: Image as numpy array.
    """

    timestamp: int
    frame_data: np.ndarray


class Camera:
    def __init__(self, simulation: Simulation, name: str) -> None:
        self.simulation = simulation
        self.name = name
        self.camera_handler = psvdds.cameraHandler(name)

    def _frame_to_numpy(self, frame: Any) -> np.ndarray:
        # ignore bad numpy typings
        return np.array(frame, copy=False)  # type: ignore

    def get_frame(self) -> CameraFrame:
        data = self.camera_handler.receive()
        return CameraFrame(
            timestamp=data.timestamp,
            frame_data=self._frame_to_numpy(data),
        )

    def add_mesh_to_labeling(self, mesh_name: str):
        self.simulation.cmd(f"{self.name}.AddLabel {mesh_name}")
