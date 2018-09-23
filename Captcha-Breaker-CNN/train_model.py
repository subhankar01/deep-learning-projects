# Importing the neccessary packages and libraries
import cv2
import pickle
import os.path
import numpy as np 
from imutils import paths 
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2d, MaxPooling2D
from keras.layers.core import Flatten, Dense
from helpers import resize_to_fit

# Letter Images Foler
LETTER_IMAGES_FOLDER = "extracted_letter_images"
MODEL_FILENAME = "captcha_model.hdf5"
MODEL_LABELS_FILENAME = "model_labels.dat"

# initialise data and labels
data = []
labels = []

# loop over the input images
for image_file in paths.list_images(LETTER_IMAGES_FOLDER):
    # Load the image and convert it to grayscale
    image = cv2.imread(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Resize the letter so it fits in a 20 * 20 pixel box
    image = resize_to_fit(image, 20, 20)

    # Add a third channel dimension to the image
    image = np.expand_dims(image, axis = 2)

    # Grab the name of the folder based on the name of the folder it was in
    label = image_file.split(os.path.sep)[-2]

    # Add the letter image and its label to training data
    data.append(image)
    labels.append(label)

# scale the raw pixel intensities to the range [0, 1]
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

# Split the training data into training and testing tests
(X_train, X_test, y_train, y_test) = train_test_split(data, labels, test_size = 0.5, random_state = 0)

# Convert the labels into one-hot encodings
lb = LabelBinarizer().fit(y_train)
y_train = lb.transform(y_train)
y_test = lb.transform(y_test)

# Save the mapping from labels to one-hot encodings
with open(MODEL_LABELS_FILENAME, "wb") as f:
    pickle.dump(lb, f)
