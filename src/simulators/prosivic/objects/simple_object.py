from dataclasses import dataclass
from typing import Dict
from uuid import uuid4

from typing_extensions import Literal

from simulators.prosivic.simulation import Simulation

SimpleObjectType = Literal[
    "box",
    "cone",
    "pyramid",
    "sphere",
]


@dataclass
class SimpleObjectDescription:
    object_name: str
    package_data_name: str


class SimpleObject:
    TYPE_TO_DESCRIPTION_MAP: Dict[SimpleObjectType, SimpleObjectDescription] = {
        "box": SimpleObjectDescription("Basic_shapes_Box", "Basic_shapes_Box.zip"),
        "cone": SimpleObjectDescription("Basic_shapes_Cone", "Basic_shapes_Cone.zip"),
        "pyramid": SimpleObjectDescription(
            "Basic_shapes_Pyramid", "Basic_shapes_Pyramid.zip"
        ),
        "sphere": SimpleObjectDescription(
            "Basic_shapes_Sphere", "Basic_shapes_Sphere.zip"
        ),
    }

    def __init__(self, simulation: Simulation, object_type: SimpleObjectType) -> None:
        self.simulation: Simulation = simulation
        self.description = self.TYPE_TO_DESCRIPTION_MAP[object_type]

        self.package_name = str(uuid4())
        self.name = f"{self.package_name}/{self.description.object_name}"

        self.simulation.create_object_from_package_data(
            package_name=self.package_name,
            package_data=self.description.package_data_name,
        )

    def set_position(self, x: float, y: float, z: float = 0) -> None:
        self.simulation.cmd(f"{self.package_name}.SetLocalPosition {x} {y} {z}")

    def delete(self) -> None:
        self.simulation.delete_object(self.package_name)
