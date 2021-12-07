from pathlib import Path

project_root_path = Path(__file__).parents[2]

example_dir_path = project_root_path / "examples"
example_data_generation_config = example_dir_path / "data-generation-config.yaml"

yolo_model = project_root_path / "models" / "yolo.pt"
