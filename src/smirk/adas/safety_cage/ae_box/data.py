#
# SMIRK
# Copyright (C) 2021-2023 RISE Research Institutes of Sweden AB
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
from typing import Tuple

import numpy as np

from yolov5.utils.augmentations import letterbox

IMG_SIZE = (160, 64)


def resize_box_img(box_img: np.ndarray, new_size: Tuple[int, int] = IMG_SIZE):
    resized_img, *_ = letterbox(box_img, new_size, auto=False, scaleFill=True)

    return resized_img


def get_init_img(img_size: Tuple[int, int] = IMG_SIZE):
    return np.random.random((1, *img_size, 3)).astype(np.float32)
