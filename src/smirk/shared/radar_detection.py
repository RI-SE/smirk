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
from dataclasses import dataclass


@dataclass
class RadarDetection:
    """A radar detection.

    Coordinates are given in the radars coordinate system.
    Origin is at the radar, y axis increasing in the direction of the radar, x axis increasing towards the right.
    Angles are given relative to the y-axis, and increase towards the right.

    Attributes:
        timestamp: Prosivic timestamp in microseconds.
        angle: Angle to object.
        distance: Distance to object.
        x: Lateral distance to object.
        y: Longitudinal distance to object.
        ttc: Time to collision in seconds.
    """

    timestamp: int
    distance: float
    angle: float
    x: float
    y: float
    ttc: float
