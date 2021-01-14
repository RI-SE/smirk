from pedestrian_generator.prosivic.prosivic_tcp import ProsivicTCP


class Simulation:
    def __init__(self, script_filename: str) -> None:
        print(f"Loading {script_filename}")
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

    def cmd(self, script_command: str) -> None:
        self.tcp.cmd(script_command)
