import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

PEAPIX_URL = os.getenv('PEAPIX_URL')


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

    def __init__(self, bing_store, location, year, month, day):

        if location in self.country_code.values():
            self.location = location
        else:
            self.location = self.country_code['United States']

        self.bing_store = bing_store
        self.year = year
        self.month = month
        self.date = datetime(year, month, day)
        self.day = self.date.strftime("%B %d")
        self.URL = f"{PEAPIX_URL}/{self.location}/{self.year}/{self.month}"
        print(self.URL)

    def get_images(self):
        date = self.date.strftime('%Y-%m-%d')

        # Find from the DB
        result = self.bing_store.find_one({ "date": date, "location": self.location })
        if result is not None:
            del result['_id']
            return result
        else:
            page = requests.get(self.URL)
            soup = BeautifulSoup(page.content, "html.parser")
            images = soup.find_all("div", class_="image-list__container")

            for image in images:

                title_element = image.find("h4", class_="image-list__title")
                date_element = image.find("span", class_="text-gray")
                url_element = image.find("div", class_="image-list__picture")

                image_title = title_element.text.strip()
                image_date = datetime.strptime(str(self.year) + " " + date_element.text, "%Y %B %d").strftime(
                    '%Y-%m-%d')
                image_url = url_element['data-bgset'].strip().replace("_480", "")

                if self.bing_store.find_one({ "date": image_date, "location": self.location }) is None:
                    print("Adding entry for ", image_date, "...")
                    result = {"title": image_title, "date": image_date,
                              "location": self.location, "url": image_url}
                    self.bing_store.insert_one(result)
                    # Do not print the _id from DB
                    del result['_id']
                    print(result)

                # Check if it's the matched date
                if self.date == image_date:
                    return result

        # If it cannot find the date then check for the Yesterday's
        self.date = datetime.today() - timedelta(days=1)
        return self.get_images()
