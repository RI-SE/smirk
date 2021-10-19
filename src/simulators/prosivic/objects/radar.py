import math
from dataclasses import dataclass
from typing import Dict, List, Optional

import ProSivicDDS as psvdds

import simulators.prosivic.utils as utils


@dataclass
class RawProsivicRadarFrame:
    """Approximation of the prosivic radar frame object."""

    id_radar: int
    distance: float
    horizontalAngularPosition: float
    reflectivity: float
    probability: float
    longtitudinalSpeed: float  # Doesn't seem to give correct values.
    lateralSpeed: float  # Doesn't seem to give correct values.
    longtitudinalAcceleration: float
    lateralAcceleration: float


@dataclass
class RawProsivicHandlerData:
    """Approximation of the object returned from prosivic radar handler."""

    timestamp: int
    nbTargetMax: int
    nbTargetDetected: int
    data: List[RawProsivicRadarFrame]


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


@dataclass
class RadarData:
    timestamp: int
    detections: List[RadarDetection]


class Radar:
    """Prosivic radar. The radar is assumed to be centered on the front of the car.

    Attributes:
        name: Name of the prosivic radar object.
        collision_width: Lateral distance for ttc calculations e.g. half car width.
    """

    def __init__(self, name: str, collision_width: float) -> None:
        self.radar_handler = psvdds.radarHandler(name)
        self.previous_detections: Dict[int, RadarDetection] = {}
        self.collision_width = collision_width

    def _calculate_ttc(
        self,
        previous_detection: Optional[RadarDetection],
        current_detection: RadarDetection,
    ) -> float:
        """Estimates time to collision

        The estimate is based on two object positions, speed and direction are assumed to be constant over time.
        """
        if not previous_detection:
            return math.inf

        delta_t = utils.timestamp_to_seconds(
            current_detection.timestamp - previous_detection.timestamp
        )

        if delta_t == 0:
            return previous_detection.ttc

        delta_y = previous_detection.y - current_detection.y

        if delta_y < 0:
            return math.inf

        delta_x = current_detection.x - previous_detection.x

        v_y = delta_y / delta_t
        v_x = delta_x / delta_t

        time_to_y0 = current_detection.y / v_y
        x_at_y0 = current_detection.x + v_x * time_to_y0

        if abs(x_at_y0) > self.collision_width:
            return math.inf

        return time_to_y0

    def _process_detection(
        self, timestamp: int, raw_detection: RawProsivicRadarFrame
    ) -> RadarDetection:
        """Parse and track detected object. Returns parsed detection."""
        object_id = raw_detection.id_radar
        angle_rad = math.radians(raw_detection.horizontalAngularPosition)

        current_detection = RadarDetection(
            timestamp,
            raw_detection.distance,
            raw_detection.horizontalAngularPosition,
            raw_detection.distance * math.sin(angle_rad),
            raw_detection.distance * math.cos(angle_rad),
            math.inf,
        )
        previous_detection = self.previous_detections.get(object_id)

        ttc = self._calculate_ttc(previous_detection, current_detection)
        current_detection.ttc = ttc
        self.previous_detections[object_id] = current_detection

        return current_detection

    def get_detections(self) -> RadarData:
        handler_data: RawProsivicHandlerData = self.radar_handler.receive()

        detections = [
            self._process_detection(handler_data.timestamp, frame)
            for frame in handler_data.data
        ]

        return RadarData(handler_data.timestamp, detections)
