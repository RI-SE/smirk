def timestamp_to_seconds(timestamp_micro: int) -> float:
    """ Converts prosivic timestamp in micro seconds to seconds"""
    return timestamp_micro / 1e6
