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

config_dir_path = project_root_path / "config"
prosivic_dds_config_path = config_dir_path / "dds.json"
