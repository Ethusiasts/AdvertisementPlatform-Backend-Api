import os
import cv2
import numpy as np
import tensorflow as tf
import requests
import urllib.request


def checkImage(image):
    # Download the image from the URL
    response = urllib.request.urlopen(image)
    image_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is not None:
        resized_image = cv2.resize(image, (50, 50))
        preprocessed_image = resized_image.astype('float32') / 255
        test_image = np.expand_dims(preprocessed_image, axis=0)

        model = tf.keras.models.load_model(os.getcwd() + '/model.h5')

        result = model.predict(test_image)
        predicted_class = np.argmax(result)

        class_labels = {
            0: "Alcohol",
            1: "Condom",
            2: "Pornography",
        }

        max_value = np.max(result)
        threshold = 15

        print("Result is:", result*10, threshold)
        if np.all(result*10 < threshold):
            print("Other")
            return 0
        else:
            predicted_label = class_labels.get(
                predicted_class, class_labels[2])
            # print("Result is:", result * 10)
            # print("It is", predicted_label)
            # print("Prediction:", predicted_class)
            print("Adult Content")
            return 1

    else:
        print("Failed to load the image.")
        return 2
