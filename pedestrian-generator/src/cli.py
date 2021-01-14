from pathlib import Path
import sys
from pedestrian_generator.data_generator import main

if __name__ == "__main__":
    config_path = Path("scenario-config.yaml")
    if not config_path.exists():
        print(f"Could not find config: {config_path.absolute()}")
        sys.exit(-1)
    main(config_path)
