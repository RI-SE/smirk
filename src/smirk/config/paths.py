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

project_root_path = Path(__file__).parents[3]

temp_dir_path = project_root_path / "temp"
default_data_dir_path = temp_dir_path / "data"

example_dir_path = project_root_path / "examples"
example_data_generation_config = example_dir_path / "data-generation-config.yaml"

default_system_test_config = (
    project_root_path / "config" / "system_tests" / "smirk-scenario-tests.yaml"
)

model_dir_path = project_root_path / "models"
yolo_model = model_dir_path / "yolo.pt"
vae_model = model_dir_path / "vae"
ae_box_model = model_dir_path / "ae_box"

config_dir_path = project_root_path / "config"
prosivic_dds_config_path = config_dir_path / "dds.json"
yolo_model_config = config_dir_path / "yolo" / "yolov5s.yaml"
yolo_model_hyp = config_dir_path / "yolo" / "hyp.yaml"
