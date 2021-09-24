import logging
import socket
import time
from typing import Optional


class ProsivicTCP:
    def __init__(self, ip: str = "127.0.0.1", port: int = 4444) -> None:
        self._ip = ip
        self._port = port
        self.log = logging
        self._socket: Optional[socket.socket] = None

    def connect(self) -> None:
        self.log.info("[ProSiVIC_TCP]: Trying to connect to TCP host .. ")
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self._ip, self._port))
        except Exception:
            self._socket = None
            time.sleep(1)
        if self._socket is None:
            self.connect()

    def step(self, steps: int = 1) -> None:
        self._send_cmd(f"COMD pass {steps}")

    def _send_cmd(self, cmd: str, wait_for_answer: bool = True) -> str:
        self.log.info("[ProSiVIC_TCP]: Executing command ... :%s" % str(cmd))
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._ip, self._port))
        self._socket.send(cmd.encode())
        if wait_for_answer:
            data = self._socket.recv(1024)
        else:
            data = b""
        self._socket.close()
        return data.decode()

    # load a script
    def load(self, script: str) -> None:
        self._send_cmd("LOAD " + script)

    # play
    def play(self) -> None:
        self._send_cmd("PLAY")

    # pause
    def pause(self) -> None:
        self._send_cmd("PAUSE")

    # stop
    def stop(self) -> None:
        self._send_cmd("STOP")

    # synchro dds
    def synchro(self) -> None:
        self._send_cmd("SYNCHRODDS")

    # execute any ProSIVIC script command example _cmd("new sivicTime timeObject")
    def cmd(self, psv_script_command: str) -> None:
        self._send_cmd("COMD " + psv_script_command)

    # Set any proSiVIC object property (example _set("time","ExportMode","Mode_on" )
    def set(
        self, psv_object_name: str, object_property_name: str, property_value: str
    ) -> None:
        self._send_cmd(
            " ".join(["SETP", psv_object_name, object_property_name, property_value])
        )

    # Get value of any proSiVIC object property (example _get("time","SimuTime")  )
    def get(self, psv_object_name: str, object_property_name: str) -> None:
        self._send_cmd("GETP " + psv_object_name + " " + object_property_name)
