from typing import Dict
from uuid import uuid4

from typing_extensions import Literal

from simulators.prosivic.simulation import Simulation

PedestrianAppearance = Literal[
    "male_business",
    "male_casual",
    "male_worker",
    "female_business",
    "female_casual",
    "child",
]


class Pedestrian:
    PROSIVIC_OBJECT_NAME = "pedestrian"
    APPEARANCE_TO_PACKAGE_DATA_MAP: Dict[PedestrianAppearance, str] = {
        "male_business": "male_smart.zip",
        "male_casual": "male_casual.zip",
        "male_worker": "male_worker.zip",
        "female_business": "female_smart.zip",
        "female_casual": "female_casual.zip",
        "child": "NCAP_Child_PT.zip",
    }
    MESH_OBJECTS = [
        "headmain",
        "hipsmain",
        "left_claviclemain",
        "left_footmain",
        "left_handmain",
        "left_lower_armmain",
        "left_lower_legmain",
        "left_upper_armmain",
        "left_upper_legmain",
        "lower_torsomain",
        "neckmain",
        "right_claviclemain",
        "right_footmain",
        "right_handmain",
        "right_lower_armmain",
        "right_lower_legmain",
        "right_upper_armmain",
        "right_upper_legmain",
        "upper_torsomain",
    ]

    def __init__(
        self,
        simulation: Simulation,
        appearance: PedestrianAppearance,
    ) -> None:
        self.simulation: Simulation = simulation
        self.appearance: PedestrianAppearance = appearance

        self.package_name = str(uuid4())
        self.name = f"{self.package_name}/{self.PROSIVIC_OBJECT_NAME}"

        self.simulation.create_object_from_package_data(
            package_name=self.package_name,
            package_data=self.APPEARANCE_TO_PACKAGE_DATA_MAP[self.appearance],
        )

        self.set_rcs_enabled(True)

    def set_rcs_enabled(self, enabled: bool) -> None:
        self.simulation.cmd(f"{self.package_name}/RCS.SetDisabled {int((not enabled))}")

    def get_mesh_names(self):
        return [f"{self.name}/{mesh_name}" for mesh_name in self.MESH_OBJECTS]

    def set_position(self, x: float, y: float, z: float = 0) -> None:
        self.simulation.cmd(f"{self.name}.SetPosition {x} {y} {z}")

    def set_angle(self, z: float) -> None:
        self.simulation.cmd(f"{self.name}.SetAngle 0 0 {z}")

    def set_speed(self, speed: float) -> None:
        self.simulation.cmd(f"{self.name}.SetSpeed {speed}")

    def delete(self) -> None:
        self.simulation.delete_object(self.package_name)
