#
# SMIRK
# Copyright (C) 2021-2023 RISE Research Institutes of Sweden AB
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import gc
from pathlib import Path

import numpy as np
import tensorflow as tf
from alibi_detect.od import OutlierAE
from alibi_detect.utils.saving import save_detector
from tensorflow.keras.layers import (
    Conv2D,
    Conv2DTranspose,
    Dense,
    Flatten,
    InputLayer,
    Reshape,
)
from tqdm import tqdm


def train(
    data_path: Path,
    out_dir: Path,
    epochs=10,
    batch_size=1024,
    seed=3,
    img_height=160,
    img_width=64,
    num_channels=3,
    encoding_dim=1024,
):

    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1.0 / 255
    ).flow_from_directory(
        str(data_path),
        batch_size=batch_size,
        class_mode=None,
        color_mode="rgb",
        target_size=(img_height, img_width),
        shuffle=True,
        seed=seed,
    )

    od = create_model(img_height, img_width, num_channels, encoding_dim)

    for e in range(epochs):
        for _ in tqdm(range(len(datagen))):
            gc.collect()
            od.fit(next(datagen), epochs=1, verbose=False)
        save_detector(od, out_dir / f"ae_box_{e}")


def create_model(img_height, img_width, num_channels, encoding_dim):
    encoder_net = tf.keras.Sequential(
        [
            InputLayer(input_shape=(img_height, img_width, num_channels)),
            Conv2D(32, 4, strides=2, padding="same", activation=tf.nn.relu),
            Conv2D(64, 4, strides=2, padding="same", activation=tf.nn.relu),
            Conv2D(
                128, 4, strides=2, padding="same", activation=tf.nn.relu, name="conv"
            ),
            Flatten(),
            Dense(encoding_dim),
        ]
    )

    conv_shape = encoder_net.get_layer("conv").output_shape[1:]

    decoder_net = tf.keras.Sequential(
        [
            InputLayer(input_shape=(encoding_dim,)),
            Dense(np.prod(conv_shape)),
            Reshape(target_shape=conv_shape),
            Conv2DTranspose(64, 4, strides=2, padding="same", activation=tf.nn.relu),
            Conv2DTranspose(32, 4, strides=2, padding="same", activation=tf.nn.relu),
            Conv2DTranspose(
                num_channels, 4, strides=2, padding="same", activation="sigmoid"
            ),
        ]
    )

    od = OutlierAE(encoder_net=encoder_net, decoder_net=decoder_net)

    return od
