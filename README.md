# Instagram Predict: First attempt

First attempt on predicting the likes a photo will get on Instagram.

Given a list of Instagram users, it downloads their latest photos with their corresponding likes and the number of their followers. Then, it creates a CNN model with **Keras** on **Tensorflow** that predicts the number of likes an image will get.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python 3.x

### Installing

Installing the requirements

```
pip install -r requirements.txt
```

## Running

1. In the *usernames.txt* write the usernames of the Instagram users you want to scrape (One per line)
1. Run `python3 scraper.py`
1. The data are now saved under */data*
1. Run `python3 Analyze/analyzer.py` to download the images under *data/download* and a create a CNN model that predicts the number of likes based on the image and the number of followers.
1. The model is saved under */models*
1. Place the images whose likes you want to predict under *Analyze/to_predict*
1. Go to *predictor.py* and add the number of followers of each image's user (line *12*)
1. Run `python3 predictor.py`

## License

This project is licensed under the GNU General Public License v3.0 License
