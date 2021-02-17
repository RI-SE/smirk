from typing import Any

import numpy as np


class SafetyCage:
    def is_accepted(self, camera_frame: np.ndarray, model_data: Any = None) -> bool:
        return True
