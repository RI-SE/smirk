from simulators.prosivic.simulation import Simulation


class Pedestrian:
    def __init__(self, name: str, simulation: Simulation) -> None:
        self.name = name
        self.simulation = simulation

    def set_position(self, x: float, y: float, z: float = 0) -> None:
        self.simulation.cmd(f"{self.name}.SetPosition {x} {y} {z}")

    def set_angle(self, z: float) -> None:
        self.simulation.cmd(f"{self.name}.SetAngle 0 0 {z}")

    def set_speed(self, speed: float) -> None:
        self.simulation.cmd(f"{self.name}.SetSpeed {speed}")
