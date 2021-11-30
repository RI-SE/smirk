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
