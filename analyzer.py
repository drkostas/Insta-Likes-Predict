import os
import sys
import pickle
import itertools
import urllib.request
import numpy as np
import cv2
import glob
from os.path import dirname, join


def downloadimages(src, destination):
    # Download images
    directory = dirname(__file__)
    src = join(directory, src)
    destination = join(directory, destination)
    if not os.path.exists(destination):
        os.makedirs(destination)
    data = pickle.load(open(src, 'rb'))
    spinner = itertools.cycle(['.', '..', '...'])
    i = 0
    for _, pictures in data.items():
        print('\rDownloading images{}'.format(next(spinner)), end="")
        for picture in pictures:
            urllib.request.urlretrieve(picture['img-small'], destination + 'img' + str(i) + '.jpeg')
            i += 1


def getlikes(src):
    # Get the likes of each photo
    directory = dirname(__file__)
    src = join(directory, src)
    data = pickle.load(open(src, 'rb'))
    likes = []
    for _, pictures in data.items():
        for picture in pictures:
            likes.append(picture['likes'])
    return np.array(likes)


def getfollowers(src):
    # Get the followers of each photo's user
    directory = dirname(__file__)
    src = join(directory, src)
    data = pickle.load(open(src, 'rb'))
    likes = []
    for _, pictures in data.items():
        for picture in pictures:
            likes.append(picture['followers'])
    return np.array(likes)


def main(argv):
	IMAGESIZE = (200, 200) 

	# Read the followers
	followers = getfollowers(src='./data/pickledump')
	followers = np.array(followers)

	# Read the likes
	likes = getlikes(src='./data/pickledump')
	likes= np.array(likes)

	# Download the images
	downloadimages(src='./data/pickledump', destination='./data/download/')
	# Read the images
	images = []
	for ind, imgfile in enumerate(glob.glob('./data/download/*.jpeg')):
	    img = cv2.imread(imgfile)
	    resized = cv2.resize(img, IMAGESIZE)
	    images.append(resized)
	images = np.array(images)

	# Transform the data
	# Analyze
	# Get Results

if __name__ == "__main__":
    sys.exit(main(sys.argv))
