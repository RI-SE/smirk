import subprocess
from pathlib import Path

import psutil


class Supervisor:
    TERMINATION_WAIT_SECONDS = 10

    def __init__(self, path: Path) -> None:
        self.path = str(path.resolve())
        self.start()

    def start(self) -> None:
        self.process = subprocess.Popen([self.path])

    def has_terminated(self) -> bool:
        return self.process.poll() is not None

    def is_runnig(self) -> bool:
        return psutil.pid_exists(self.process.pid)

    def restart(self) -> None:
        if self.is_runnig():
            self.terminate()
            self.process.wait(self.TERMINATION_WAIT_SECONDS)

        self.start()

    def terminate(self) -> None:
        self.process.terminate()
