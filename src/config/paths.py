from pathlib import Path

project_root_path = Path(__file__).parents[2]

# TODO: Extract and load things that should be user configurable.
prosivic_exe_path = Path(
    r"C:\Program Files\ESI Group\Pro-SiVIC\2020.0\bin\Win64.Release\Pro-SiVIC.exe"
)

example_dir_path = project_root_path / "examples"
example_data_generation_config = example_dir_path / "data-generation-config.yaml"

model_dir_path = project_root_path / "models"
yolo_model = model_dir_path / "yolo.pt"
vae_model = model_dir_path / "vae"

config_dir_path = project_root_path / "config"
prosivic_dds_config_path = config_dir_path / "dds.json"
