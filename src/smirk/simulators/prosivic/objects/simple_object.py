#
# SMIRK
# Copyright (C) 2021-2022 RISE Research Institutes of Sweden AB
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
from dataclasses import dataclass
from typing import Dict
from uuid import uuid4

from typing_extensions import Literal

from smirk.simulators.prosivic.simulation import Simulation

SimpleObjectType = Literal["box", "cone", "pyramid", "sphere", "cylinder"]


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
        "cylinder": SimpleObjectDescription(
            "Basic_shapes_Cylinder", "Basic_shapes_Cylinder.zip"
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

        self.rcs_name = f"{self.package_name}_RCS"
        self.simulation.create_object("sivicRCS", self.rcs_name)
        self.simulation.cmd(f"{self.rcs_name}.SetParent {self.name}")
        self.simulation.cmd(f"{self.rcs_name}.SetLocalPosition 0 0 0")

    def set_position(self, x: float, y: float, z: float = 0) -> None:
        self.simulation.cmd(f"{self.package_name}.SetLocalPosition {x} {y} {z}")

    def delete(self) -> None:
        self.simulation.delete_object(self.rcs_name)
        self.simulation.delete_object(self.package_name)

    def get_mesh_names(self):
        return [self.name]
