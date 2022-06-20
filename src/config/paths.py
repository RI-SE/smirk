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
from pathlib import Path

project_root_path = Path(__file__).parents[2]

# TODO: Allow configuring this somewhere else?
prosivic_exe_path = Path(
    r"C:\Program Files\ESI Group\Pro-SiVIC\2020.0\bin\Win64.Release\Pro-SiVIC.exe"
)
prosivic_projects_folder = Path(r"C:\Users\eitn35\Pro-SiVIC\My project")
prosivic_sensor_folder = prosivic_projects_folder / "sensors"
prosivic_distance_out_filename = "collision_observer.csv"

temp_dir_path = project_root_path / "temp"

example_dir_path = project_root_path / "examples"
example_data_generation_config = example_dir_path / "data-generation-config.yaml"

model_dir_path = project_root_path / "models"
yolo_model = model_dir_path / "yolo.pt"
vae_model = model_dir_path / "vae"
ae_box_model = model_dir_path / "ae_box"

config_dir_path = project_root_path / "config"
prosivic_dds_config_path = config_dir_path / "dds.json"
