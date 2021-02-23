import logging

from smirk.car.car import Car
from smirk.pedestrian_detector.pedestrian_detector import PedestrianDetector
from smirk.safety_cage.safety_cage import SafetyCage


class Smirk:
    TTC_THRESHOLD_MILLIS = 4000

    def __init__(
        self, car: Car, pedestrian_detector: PedestrianDetector, safety_cage: SafetyCage
    ):
        self.car = car
        self.pedestrian_detector = pedestrian_detector
        self.safety_cage = safety_cage

    def start_detector(self):
        while True:
            logging.info("Checking radar.")
            radar_detections = self.car.get_radar_reading()
            is_ttc_below_threshold = any(
                detection.time_to_collision < self.TTC_THRESHOLD_MILLIS
                for detection in radar_detections
            )

            if not is_ttc_below_threshold:
                logging.info("No detections within range.")
                continue

            logging.info("Running pedestrian detection.")
            current_camera_frame = self.car.get_camera_frame()
            is_pedestrian = self.pedestrian_detector.is_pedestrian(current_camera_frame)

            if not is_pedestrian:
                logging.info("No pedestrians found.")
                continue

            logging.info("Running safety cage.")
            is_accepted_by_safety_cage = self.safety_cage.is_accepted(
                current_camera_frame
            )

            if not is_accepted_by_safety_cage:
                logging.info("Rejected by safety cage.")
                continue

            logging.info("Braking.")
            self.car.brake()
