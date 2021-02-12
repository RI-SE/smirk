from absl import flags
from object_detection import model_lib_v2
import tensorflow as tf
from pathlib import Path
import shutil
from typing import Dict

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

TRAINED_BASE_DIR = Path("./trained")
PRE_TRAINED_BASE_DIR = Path("./pre-trained")


def load_model(pre_train_base_dir: Path, model_config: Dict) -> None:
    if Path(pre_train_base_dir / model_config["name"]).exists():
        print(f"Using cached model")

    else:
        tf.keras.utils.get_file(
            fname=model_config["name"],
            origin=model_config["url"],
            extract=True,
            archive_format="tar",
            cache_dir=pre_train_base_dir,
        )

        shutil.move(
            pre_train_base_dir / "datasets" / model_config["origin_name"],
            pre_train_base_dir / model_config["name"],
        )


def train(
    trained_dir: Path, train_steps, checkpoint_every_n, checkpoint_max_to_keep
) -> None:
    tf.config.set_soft_device_placement(True)
    strategy = tf.compat.v2.distribute.MirroredStrategy()

    with strategy.scope():
        model_lib_v2.train_loop(
            pipeline_config_path=trained_dir / "pipeline.config",
            model_dir=trained_dir,
            train_steps=train_steps,
            checkpoint_every_n=checkpoint_every_n,
            checkpoint_max_to_keep=checkpoint_max_to_keep,
        )


flags.DEFINE_enum("model_name", None, MODELS.keys(), "The model to train.")
flags.DEFINE_integer("train_steps", None, "Override number of trainig steps.")
flags.DEFINE_integer("checkpoint_every_n", 1000, "Number of steps between checkpoints.")
flags.DEFINE_integer(
    "checkpoint_max_to_keep", 5, "Maximum number of checkpoints to keep i.e. n latest."
)

FLAGS = flags.FLAGS


def main(_):
    flags.mark_flag_as_required("model_name")

    model_config = MODELS[FLAGS.model_name]
    load_model(PRE_TRAINED_BASE_DIR, model_config)
    train(
        TRAINED_BASE_DIR / model_config["name"],
        train_steps=FLAGS.train_steps,
        checkpoint_every_n=FLAGS.checkpoint_every_n,
        checkpoint_max_to_keep=FLAGS.checkpoint_max_to_keep,
    )


if __name__ == "__main__":
    tf.compat.v1.app.run()
