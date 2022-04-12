import ProSivicDDS as psvdds

import config.paths
from simulators.prosivic.prosivic_tcp import ProsivicTCP


class Simulation:
    def __init__(self) -> None:
        self.tcp = ProsivicTCP()
        self.tcp.connect()

        psvdds.initcomms(str(config.paths.prosivic_dds_config_path.resolve()))

    def play(self) -> None:
        self.tcp.play()

    def pause(self) -> None:
        self.tcp.pause()

    def stop(self) -> None:
        self.tcp.stop()

    def step(self, steps: int) -> None:
        self.tcp.step(steps)

    def cmd(self, script_command: str) -> None:
        self.tcp.cmd(script_command)

    def create_object(self, type: str, name: str, dds=False) -> None:
        self.cmd(f"new {type} {name}")

        if dds:
            self.cmd(f"{name}.SetOMGDDSEnabled true")
            self.cmd(f"{name}.On")

    def create_object_from_package_data(self, package_name, package_data) -> None:
        self.create_object("sivicPackage", package_name)
        self.cmd(f"{package_name}.SetPackageData {package_data}")

    def delete_object(self, object_name: str) -> None:
        self.cmd(f"delete {object_name}")

    def set_simulation_name(self, name: str) -> None:
        self.cmd(f"setsimulationname {name}")

    def load_scene(self, script_filename: str):
        self.clear()
        self.tcp.load(script_filename)

    def clear(self):
        self.stop()
        self.cmd("clear")
        self.cmd("cleanup")

    def get(self, psv_object_name: str, object_property_name: str) -> str:
        return self.tcp.get(psv_object_name, object_property_name)
