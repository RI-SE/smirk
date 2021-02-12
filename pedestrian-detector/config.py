from pathlib import Path

TRAINED_BASE_DIR = Path("./trained")
PRE_TRAINED_BASE_DIR = Path("./pre-trained")

MODELS = {
    "efficient-det-d0": {
        "origin_name": "efficientdet_d0_coco17_tpu-32",
        "name": "efficient-det-d0",
        "url": "http://download.tensorflow.org/models/object_detection/tf2/20200711/efficientdet_d0_coco17_tpu-32.tar.gz",
    },
    "ssd_mobilenet_320": {
        "origin_name": "ssd_mobilenet_v2_320x320_coco17_tpu-8",
        "name": "ssd_mobilenet_320",
        "url": "http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_320x320_coco17_tpu-8.tar.gz",
    },
}
