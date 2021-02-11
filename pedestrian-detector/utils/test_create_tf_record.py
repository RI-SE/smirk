from pathlib import Path

from PIL import Image
import numpy as np
import pandas as pd
import tensorflow as tf

from create_tf_record import create_tf_example


class CreateTFRecordTest(tf.test.TestCase):
    def _assertProtoListSingleEqual(self, proto_field, expectation):
        self.assertListEqual(list(proto_field), [expectation])

    def test_single_example(self):
        with self.session():
            filename = "pedestrian.jpg"
            img_path = Path(self.get_temp_dir()) / "pedestrian.jpg"
            Image.fromarray(np.random.rand(256, 256, 3), "RGB").save(img_path)
            labels = pd.DataFrame(
                [
                    {
                        "img_path": str(img_path),
                        "filename": filename,
                        "width": 200,
                        "height": 100,
                        "xmin": 0,
                        "ymin": 0,
                        "xmax": 50,
                        "ymax": 50,
                        "class_text": "pedestrian",
                        "class_label": 1,
                    }
                ]
            )

            for row in labels.itertuples():
                example = create_tf_example(row)
                self._assertProtoListSingleEqual(
                    example.features.feature["image/width"].int64_list.value, 200
                )
                self._assertProtoListSingleEqual(
                    example.features.feature["image/height"].int64_list.value, 100
                )
                self._assertProtoListSingleEqual(
                    example.features.feature["image/filename"].bytes_list.value,
                    filename.encode("utf-8"),
                )
                self._assertProtoListSingleEqual(
                    example.features.feature["image/source_id"].bytes_list.value,
                    filename.encode("utf-8"),
                )
                self._assertProtoListSingleEqual(
                    example.features.feature["image/format"].bytes_list.value, b"jpeg"
                )
                self._assertProtoListSingleEqual(
                    example.features.feature["image/object/bbox/xmin"].float_list.value,
                    0,
                )
                self._assertProtoListSingleEqual(
                    example.features.feature["image/object/bbox/ymin"].float_list.value,
                    0,
                )
                self._assertProtoListSingleEqual(
                    example.features.feature["image/object/bbox/xmax"].float_list.value,
                    0.25,
                )
                self._assertProtoListSingleEqual(
                    example.features.feature["image/object/bbox/ymax"].float_list.value,
                    0.5,
                )
                self._assertProtoListSingleEqual(
                    example.features.feature[
                        "image/object/class/text"
                    ].bytes_list.value,
                    b"pedestrian",
                )
                self._assertProtoListSingleEqual(
                    example.features.feature[
                        "image/object/class/label"
                    ].int64_list.value,
                    1,
                )


if __name__ == "__main__":
    tf.test.main()
