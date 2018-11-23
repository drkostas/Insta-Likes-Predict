import sys
import time
import re
import pickle
import json
from termcolor import colored
import colorama
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Initialize colored print
colorama.deinit()
colorama.init(strip=False)


def scrape_photos(driver, photo_links, thumbnails, numfollowers):
    userdata = []
    # For each of his/her pictures
    for index, link in enumerate(photo_links):
        try:
            # Wait for the photo's page to load
            driver.get(link)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Kj7h1')))
            soup = BeautifulSoup(driver.page_source, 'lxml')

            # Get the link to the full image
            head = soup.find('head')
            image = soup.find_all('img', class_="FFVAD", limit=1)[0]
            imglarge = image["src"]

            # Get the number of likes of the picture
            liketag = head.find('meta', attrs={'property': 'og:description'})
            text = liketag.attrs["content"]
            numlikes = int(re.findall('(([0-9],{0,1})+)', text)[0][0].replace(",",""))
            print(colored("Photo: {}. Likes: {}".format(link, numlikes), "magenta"))

            # Save the links to high and low quality versions of pictures and the number of likes, followers
            userdata.append({'img-large': imglarge,
                             'img-small': thumbnails[index],  
                             'likes': numlikes,
                             'followers': numfollowers})

        except BaseException as e:
            print(colored("Photo Error: ", e.args, "magenta"))
            print(colored("Info about errored photo:", "magenta"))
            print(colored("Link: {}. liketag: {}".format(link, liketag), "magenta"))

    return userdata


def scrape_users(driver, usernames):
    full_data = {}
    # For each user
    for index, username in enumerate(usernames):
        try:
            # Create the link to the user's profile
            print(colored('\n\n\rScraping {}: {}/{}'.format(username, index+1, len(usernames)), "red"))
            baseurl = 'https://www.instagram.com'
            link = baseurl + '/' + username            

            # Wait for user's page to load
            driver.get(link)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'v9tJq')))
            soup = BeautifulSoup(driver.page_source, 'lxml')

            # If account is private, skip
            if len(soup.body.findAll(text='This Account is Private')) > 0:
                print(colored("This Account is Private. Skipping..", "cyan"))
                continue

            # Get the numbers of his/her followers
            followers_span = soup.find('meta', attrs={'property': 'og:description'})
            followers_text = followers_span.attrs["content"]
            numfollowers = int(re.findall('(([0-9],{0,1})+)', followers_text)[0][0].replace(",","")) 

            # Get the anchors of his pictures
            span = soup.find('span', attrs={'id': 'react-root'})
            posts = span.select('div[class$="_bz0w"]')        
            pictures_out = list(filter(lambda p: p.find('span', class_='glyphsSpriteVideo_large') is None, posts)) # filter out videos
            pictures = []
            [pictures.extend(elem.select('a')) for elem in pictures_out]

            # Get the links to the thumbnails of his/her pictures
            thumbnails = list(map(lambda p: p.find_all('img', class_="FFVAD", limit=1)[0]["src"], pictures))

            # Get the links to the pages of the actual photos
            photo_links = list(map(lambda p: baseurl + p['href'], pictures))
            print(colored("Followers: {}. Number of Photo Links = {}".format(numfollowers, len(photo_links)), "cyan"))

            # Scape Photos
            full_data[username] = scrape_photos(driver, photo_links, thumbnails, numfollowers)

        except BaseException as e:
            print(colored("User Error: ", e.args, "cyan"))
            print(colored("Info about errored user:", "cyan"))
            print(colored("Link: {}.".format(link), "cyan"))

    return full_data

def main(argv):
    print(argv)
    # Initialize Web Driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)

    # Load the usernames
    usernamesfile = open('usernames.txt', 'r')
    usernames = usernamesfile.read().split('\n')

    # Scrape Users
    full_data = scrape_users(driver, usernames) 

    # Close the webdriver
    driver.quit()

    # Save the data to a json file
    with open('./data/scraped.json', 'w') as outfile:
        datastr = json.dumps(full_data, indent=4, sort_keys=True)
        outfile.write(datastr)
    print(colored("\n\nData saved to scraped.json succesfully.","yellow"))

    # Save the data to a pickle file as a backup
    with open('./data/pickledump', 'wb') as picklefile:
        pickle.dump(full_data, picklefile)
    print(colored("Data saved to pickledump succesfully.","yellow"))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
