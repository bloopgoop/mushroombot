import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

from sklearn.model_selection import train_test_split


model = load_model('model')

img_file = 'data/0/1x5a.jpg'

#img = image.load_img(img_file, target_size = (25, 25))
#img_array = image.img_to_array(img)
#img_array = np.expand_dims(img_array, axis=0)
#predictions = model.predict(img_array)

#print(predictions)
#best_prediction_index = np.argmax(predictions)

# labels
#class_labels = ['class_0', 'class_1', 'class_2', ...]  # List of class labels in the same order as during training
#best_prediction_label = class_labels[best_prediction_index]

#print(best_prediction_index)
print(model.input_shape)