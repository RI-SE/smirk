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

TIMESTAMP_PER_SECOND = 1e6


def timestamp_to_seconds(timestamp_micro: int) -> float:
    """Converts prosivic timestamp in micro seconds to seconds"""
    return timestamp_micro / TIMESTAMP_PER_SECOND


def ms_to_kmh(speed_ms: float) -> float:
    """Converts meters per second to kilometers per hour."""
    return speed_ms * 3.6


def kmh_to_ms(speed_kmh: float) -> float:
    """Converts kilometers per hour to meters per second."""
    return speed_kmh / 3.6
