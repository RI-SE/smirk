import logging
import os

import numpy as np
from PIL import Image, ImageDraw

from smirk.car import car, radar_detection
from smirk.car.fake_car import (
    fake_brakes,
    fake_camera,
    fake_radar,
    fake_sensor_exception,
)
from smirk.pedestrian_detector.ssd_hub_detector import SsdHubDetector
from smirk.safety_cage.safety_cage import SafetyCage

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from smirk.smirk import Smirk  # noqa: E402

logging.basicConfig(level=logging.INFO)


def draw_detection_bbox(camera_frame: np.ndarray, boxes: np.ndarray):
    image = Image.fromarray(camera_frame)
    width, height = image.size
    draw = ImageDraw.Draw(image)

    for ymin, xmin, ymax, xmax in boxes:
        draw.rectangle([xmin * width, ymin * height, xmax * width, ymax * height])

    image.show()
    input("Press enter to continue...")


camera = fake_camera.FakeCamera(
    [
        "./example_images/01.jpg",
        "./example_images/02.jpg",
        "./example_images/03.jpg",
    ]
)
radar = fake_radar.FakeRadar(
    [radar_detection.RadarDetection(None, ttc) for ttc in [4000, 3000, 2000, 1000]]
)
brakes = fake_brakes.FakeBrakes()

fake_car = car.Car(radar, camera, brakes)
detector = SsdHubDetector(debug_fn=draw_detection_bbox)
safety_cage = SafetyCage()

smirk = Smirk(fake_car, detector, safety_cage)

try:
    smirk.start_detector()
except fake_sensor_exception.FakeSensorException:
    logging.info("DONE")
