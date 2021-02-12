from pathlib import Path

from object_detection.utils import dataset_util
import pandas as pd
import tensorflow as tf
from tqdm import tqdm


def create_tf_example(example):
    with tf.io.gfile.GFile(example.img_path, "rb") as f:
        encoded_img = f.read()

    example = tf.train.Example(
        features=tf.train.Features(
            feature={
                "image/height": dataset_util.int64_feature(example.height),
                "image/width": dataset_util.int64_feature(example.width),
                "image/filename": dataset_util.bytes_feature(
                    example.filename.encode("utf-8")
                ),
                "image/source_id": dataset_util.bytes_feature(
                    example.filename.encode("utf-8")
                ),
                "image/encoded": dataset_util.bytes_feature(encoded_img),
                "image/format": dataset_util.bytes_feature(b"jpeg"),
                "image/object/bbox/xmin": dataset_util.float_feature(
                    example.xmin / example.width
                ),
                "image/object/bbox/xmax": dataset_util.float_feature(
                    example.xmax / example.width
                ),
                "image/object/bbox/ymin": dataset_util.float_feature(
                    example.ymin / example.height
                ),
                "image/object/bbox/ymax": dataset_util.float_feature(
                    example.ymax / example.height
                ),
                "image/object/class/text": dataset_util.bytes_feature(
                    example.class_text.encode("utf-8")
                ),
                "image/object/class/label": dataset_util.int64_feature(
                    example.class_label
                ),
            }
        )
    )
    return example


def create_tf_record(data_path: Path, output_path: Path):
    labels = pd.read_csv(data_path / "labels.csv")
    labels["img_path"] = labels.filename.apply(
        lambda filename: str(data_path / filename)
    )
    writer = tf.io.TFRecordWriter(str(output_path))

    for row in tqdm(labels.itertuples(), total=len(labels)):
        tf_example = create_tf_example(row)
        writer.write(tf_example.SerializeToString())

    writer.close()


def main():
    data_path = Path("./data")

    create_tf_record(data_path / "train", data_path / "train.tfrecord")
    create_tf_record(data_path / "test", data_path / "test.tfrecord")


if __name__ == "__main__":
    main()
