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
