# Instagram Scraper

Given a list of Instagram users, it downloads their latest photos with their corresponding likes and the number of their followers. For **Data Analysis** purposes.

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

1. In the *usernames.txt* write the usernames of the instagram users you want to scrape (One per line)
1. Run `python3 scraper.py`
1. The data are now saved under */data*
1. Run `python3 analyzer.py` to download the images under *data/download* and load them along with the likes and the followers
1. Analyze them as you want!

## License

This project is licensed under the GNU General Public License v3.0 License