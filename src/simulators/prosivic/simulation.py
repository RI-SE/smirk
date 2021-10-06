from simulators.prosivic.prosivic_tcp import ProsivicTCP


class Simulation:
    def __init__(self, script_filename: str) -> None:
        self.tcp = ProsivicTCP()
        self.tcp.connect()
        self.tcp.load(script_filename)
        self.tcp.synchro()

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

    def create_object(self, name: str, type: str) -> None:
        self.cmd(f"new {type} {name}")

    def create_object_from_package_data(self, package_name, package_data) -> None:
        self.create_object(package_name, "sivicPackage")
        self.cmd(f"{package_name}.SetPackageData {package_data}")

    def delete_object(self, object_name: str) -> None:
        self.cmd(f"delete {object_name}")
