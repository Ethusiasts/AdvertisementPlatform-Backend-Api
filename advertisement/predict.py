# import os
# import cv2
# import numpy as np
# import tensorflow as tf


# image_path = os.path.join(os.getcwd(), "CNN/data/dd.jpg")
# image = cv2.imread(image_path)


# def checkImage(image):
#     if image is not None:
#         resized_image = cv2.resize(image, (50, 50))
#         preprocessed_image = resized_image.astype('float32') / 255
#         test_image = np.expand_dims(preprocessed_image, axis=0)

#         model = tf.keras.models.load_model(os.getcwd() + '/model.h5')

#         result = model.predict(test_image)
#         predicted_class = np.argmax(result)

#         class_labels = {
#             0: "Alcohol",
#             1: "Condom",
#             2: "Pornography",
#         }

#         predicted_label = class_labels.get(predicted_class, class_labels[2])

#         if result[0][0] < 10 and result[0][1] < 10 and result[0][2] < 10:
#             print("Other")
#             return 0

#         else:
#             print("Result is:", result*10)
#             print("It is", predicted_label)
#             print("Prediction:", predicted_class)
#             return 1

#     else:
#         print("Failed to load the image.")
#         return 2
