def timestamp_to_seconds(timestamp_micro: int) -> float:
    """ Converts prosivic timestamp in micro seconds to seconds"""
    return timestamp_micro / 1e6


def ms_to_kmh(speed_ms: float) -> float:
    """ Converts meters per second to kilometers per hour."""
    return speed_ms * 3.6


def kmh_to_ms(speed_kmh: float) -> float:
    """ Converts kilometers per hour to meters per second."""
    return speed_kmh / 3.6
