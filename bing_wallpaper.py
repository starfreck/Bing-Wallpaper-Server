#!/usr/bin/python3

import os
import requests
from pysondb import db as database

import datetime
from bs4 import BeautifulSoup


class BingWallpaper:
    # Valid countries
    country_code = {
        "Australia": "au",
        "Canada": "ca",
        "China": "cn",
        "Germany": "de",
        "France": "fr",
        "India": "in",
        "Japan": "jp",
        "Spain": "es",
        "United Kingdom": "gb",
        "United States": "us",
        "Italy": "it",
    }

    def __init__(self, country_name, year, month, day):

        if country_name in self.country_code:
            self.location = self.country_code[country_name]
        else:
            self.location = self.country_code['United States']

        self.year = year
        self.month = month
        self.date = x = datetime.datetime(year, month, day)

        self.day = self.date.strftime("%B %d")

        self.URL = f"https://peapix.com/bing/{self.location}/{self.year}/{self.month}"

        self.IMG_DIR = "/images"
        self.DB_DIR = "./bing-wallpaper"
        self.DB_FILE = "/db.json"

        self.FULL_DB_DIR_PATH = self.DB_DIR
        self.FULL_IMG_DIR_PATH = self.FULL_DB_DIR_PATH + self.IMG_DIR
        self.FULL_DB_FILE_PATH = self.FULL_DB_DIR_PATH + self.DB_FILE

    # Functions
    def create_db_folder(self):
        # If "bing-wallpaper" folder doesn't exist, then create it.
        if not os.path.isdir(self.FULL_DB_DIR_PATH):
            os.makedirs(self.FULL_DB_DIR_PATH)
            print("created folder : ", self.FULL_DB_DIR_PATH)
        else:
            print(self.FULL_DB_DIR_PATH, "folder already exists.")

        # If "image" folder doesn't exist, then create it.
        if not os.path.isdir(self.FULL_IMG_DIR_PATH):
            os.makedirs(self.FULL_IMG_DIR_PATH)
            print("created folder : ", self.FULL_IMG_DIR_PATH)
        else:
            print(self.FULL_IMG_DIR_PATH, "folder already exists.")

    def create_db_file(self):
        if os.path.exists(self.FULL_DB_FILE_PATH):
            if os.path.isfile(self.FULL_DB_FILE_PATH):
                print("file already exists.")
        else:
            print("created file : ", self.FULL_DB_FILE_PATH)
            open(self.FULL_DB_FILE_PATH, "w").close()

    def get_images(self):

        # Get DB
        db = database.getDb(self.FULL_DB_FILE_PATH)
        date = self.date.strftime('%Y-%m-%d')

        result = db.getBy({"date": date})
        if result:
            return result
        else:
            print(self.URL)
            page = requests.get(self.URL)
            soup = BeautifulSoup(page.content, "html.parser")
            images = soup.find_all("div", class_="image-list__container")

            # Get DB
            db = database.getDb(self.FULL_DB_FILE_PATH)

            for image in images:

                title_element = image.find("h4", class_="image-list__title")
                date_element = image.find("span", class_="text-gray")
                url_element = image.find("div", class_="image-list__picture")

                # Check if it's the matched date
                if self.day == date_element.text:

                    title = title_element.text.strip()
                    date = self.date.strftime('%Y-%m-%d')
                    url = url_element['data-bgset'].strip().replace("_480", "")

                    if not db.getBy({"date": date}):
                        print("Adding entry for ", date, "...")
                        result = {"title": title, "date": date, "location": self.location, "url": url}
                        db.add(result)
                        self.download_wallpaper(result)
                        return result

    def download_wallpaper(self, info):
        print("Downloading the wallpaper....")

        print("Title", info['title'])
        print("Date", info['date'])

        img = self.FULL_IMG_DIR_PATH + "/" + info['date'] + "_" + self.location + ".jpg"

        # Download the Wallpaper is not exists
        if not os.path.exists(img):
            downloaded_obj = requests.get(info['url'])
            with open(img, "wb") as file:
                file.write(downloaded_obj.content)

    def main(self):
        self.create_db_folder()
        return self.get_images()
