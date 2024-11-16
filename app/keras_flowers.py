import os

import tensorflow as tf
import numpy as np
from PIL import Image
from tensorflow.keras.models import Model

model_input_shape = (224, 224)
dir_path = os.path.dirname(os.path.realpath(__file__))

model = tf.keras.Sequential(layers=[
    tf.keras.Input(shape=(*model_input_shape, 3)),
    tf.keras.applications.DenseNet201(weights=None, include_top=False),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(104, activation='softmax')
])
model.load_weights(f"{dir_path}/model/keras_flower_weights.h5")

labels = np.loadtxt(f"{dir_path}/model/keras_flower_labels_fix.txt", dtype='str', delimiter=",")
embed_model = Model(inputs=model.layers[0].input, outputs=model.layers[-2].output)


def __get_img_from_path(img_path):
    return Image.open(img_path).resize(model_input_shape)


def __get_img(image):
    image = np.array(image)
    image = image / 255.0
    return np.expand_dims(image, axis=0)


def predict(image):
    results = model.predict(__get_img(image))[0]
    return results


def embed(image):
    return embed_model.predict(__get_img(image))[0]


def embed_by_path(img_file):
    return embed(__get_img_from_path(img_file))


def predict_by_path(act_path):
    return predict(__get_img_from_path(act_path))


def get_label_score(results, top):
    return sorted(zip(labels, results), key=lambda x: x[1], reverse=True)[:top]


def predict_name(image_array, top=1):
    results = predict(image_array)
    return get_label_score(results, top)


def predict_name_by_path(act_path, top=1):
    results = predict_by_path(act_path)
    return get_label_score(results, top)
