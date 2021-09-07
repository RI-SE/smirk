from dataclasses import dataclass
from typing import Any

import numpy as np
import ProSivicDDS as psvdds


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
    def __init__(self, name: str) -> None:
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
