import time
from typing import Optional


class TimerError(Exception):
    pass


class Timer:
    def __init__(self) -> None:

        self._start_time: Optional[float] = None

    def start(self) -> float:
        self._start_time = time.perf_counter()

        return self._start_time

    def lap(self) -> float:
        if self._start_time is None:
            raise TimerError("Timer not started.")

        return time.perf_counter() - self._start_time

    def stop(self) -> float:
        elapsed = self.lap()
        self.reset()
        return elapsed

    def reset(self) -> None:
        self._start_time = None
