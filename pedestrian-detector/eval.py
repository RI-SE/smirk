from pathlib import Path

from absl import flags
from object_detection import model_lib_v2
from object_detection import inputs
from object_detection import model_lib
import tensorflow as tf

import config


MODEL_BUILD_UTIL_MAP = model_lib.MODEL_BUILD_UTIL_MAP


def eval_all_checkpoints(
    pipeline_config_path: Path,
    model_dir: Path,
    checkpoint_dir: Path,
) -> None:
    get_configs_from_pipeline_file = MODEL_BUILD_UTIL_MAP[
        "get_configs_from_pipeline_file"
    ]

    configs = get_configs_from_pipeline_file(
        str(pipeline_config_path), config_override=None
    )
    model_config = configs["model"]
    eval_config = configs["eval_config"]
    eval_input_config = configs["eval_input_configs"][0]

    strategy = tf.distribute.get_strategy()
    with strategy.scope():
        detection_model = MODEL_BUILD_UTIL_MAP["detection_model_fn_base"](
            model_config=model_config, is_training=True
        )

    eval_input = strategy.experimental_distribute_dataset(
        inputs.eval_input(
            eval_config=eval_config,
            eval_input_config=eval_input_config,
            model_config=model_config,
            model=detection_model,
        )
    )

    global_step = tf.Variable(0, trainable=False, dtype=tf.dtypes.int64)

    for checkpoint_path in tf.train.get_checkpoint_state(
        str(checkpoint_dir)
    ).all_model_checkpoint_paths:
        ckpt = tf.train.Checkpoint(step=global_step, model=detection_model)

        ckpt.restore(checkpoint_path).expect_partial()

        summary_writer = tf.summary.create_file_writer(
            str(model_dir / "eval" / eval_input_config.name)
        )
        with summary_writer.as_default():
            model_lib_v2.eager_eval_loop(
                detection_model,
                configs,
                eval_input,
                global_step=global_step,
            )


flags.DEFINE_enum("model_name", None, config.MODELS.keys(), "The model to train.")

FLAGS = flags.FLAGS


def main(_):
    flags.mark_flag_as_required("model_name")
    model_dir = config.TRAINED_BASE_DIR / FLAGS.model_name

    eval_all_checkpoints(
        pipeline_config_path=model_dir / "pipeline.config",
        model_dir=model_dir,
        checkpoint_dir=model_dir,
    )


if __name__ == "__main__":
    tf.compat.v1.app.run()
