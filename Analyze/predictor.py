import sys
from os.path import dirname, join
import numpy as np
import cv2
import glob
from keras.models import load_model
import tensorflow as tf
from model import *

MODEL_VERSION = 1
IMAGESIZE = (200, 200)
FOLLOWERS = []  # Insert the number of followers of each image's user (image alphabetical order)

def read_resize(image_paths):
    # parse and resize images to use in predictions

    images = []
    for image in image_paths:
        parsed = cv2.imread(image)
        resized = cv2.resize(parsed, (IMAGESIZE[0], IMAGESIZE[1]))
        images.append(resized)

    return np.array(images)


def get_prediction(graph, model, images, followers):
    followers = np.array(followers)
    followers = (followers - np.mean(followers))/np.std(followers)  # normalize

    with graph.as_default():
        pred = model.predict([images, followers])
        return [el[0] for el in pred.tolist()]


def main(argv):
    graph = tf.get_default_graph()
    directory = dirname(__file__)
    modelpath = join(directory, '../models/regv{}.h5'.format(MODEL_VERSION))
    model = load_model(modelpath, custom_objects={'rmse': rmse, "r_square": r_square})

    # Get the paths of images to predict
    image_paths = list(glob.glob('./to_predict/*.*'))
    # Get the images as an numpy array
    images = read_resize(image_paths)

    # Predict the images
    results = get_prediction(graph, model, images, np.array(FOLLOWERS))
    print("Scores: ", dict(zip(image_paths, results)))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
