import os
import re
import requests
from datetime import datetime, timedelta
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
        "Brazil": "br",
    }
    # Headers for the request
    headers = {"User-Agent": os.getenv('USER_AGENT') }
    # Valid regex patterns
    image_regex = re.compile(r'<div class="image-list__container">([\s\S]*?)</div>')
    title_regex = re.compile(r'<h4 class="image-list__title">([\s\S]*?)</h4>')
    date_regex  = re.compile(r'<span class="text-gray">([\s\S]*?)</span>')
    url_regex   = re.compile(r'data-bgset="([\s\S]*?)"')

    def __init__(self, bing_store, location, year, month, day):

        if location in self.country_code.values():
            self.location = location
        else:
            self.location = self.country_code['United States']

        self.bing_store = bing_store
        self.year       = year
        self.month      = month
        self.date       = datetime(year, month, day)
        self.day        = self.date.strftime("%B %d")
        self.URL        = f"{PEAPIX_URL}/{self.location}/{self.year}/{self.month}"

        print(self.URL)

    def get_image_from_web(self):
        response = None

        page    = requests.get(self.URL, headers=self.headers)
        html    = page.content.decode('utf-8')

        # Find all matches for each pattern
        image_matches   = self.image_regex.findall(html)
        title_matches   = self.title_regex.findall(html)
        date_matches    = self.date_regex.findall(html)
        url_matches     = self.url_regex.findall(html)

        title_matches   = [title.strip() for title in title_matches]
        date_matches    = [datetime.strptime(str(self.year) + " " + date, "%Y %B %d").strftime('%Y-%m-%d') for date in date_matches]
        url_matches     = [url.strip().replace("_480", "") for url in url_matches]

        # Extract information from the matches
        images = []

        for i in range(len(image_matches)):
            url = url_matches[i].split(' ')[0]
            images.append({
                'title' : title_matches[i].strip(),
                'date'  : date_matches[i].strip(),
                'url'   : url
            })

        # Print the extracted information
        for image in images:
            # Check if it's already in the DB
            if self.bing_store.find_one({"date": image['date'], "location": self.location}) is None:
                print("Adding entry for ", image['date'], "...")
                result = {"title": image['title'], "date": image['date'], "location": self.location, "url": image['url']}
                self.bing_store.insert_one(result)
                # Do not print the _id from DB
                del result['_id']
                print(result)

            # Check if it's the matched date then store it and return it later
            if image['date'] == self.date.strftime('%Y-%m-%d'):
                response = result

        return response

    def get_images(self):

        # Find from the DB
        result = self.bing_store.find_one({"date": self.date.strftime('%Y-%m-%d'), "location": self.location})
        
        if result is not None:
            del result['_id']
            return result
        else:
            response = self.get_image_from_web()
            if response is not None:
                return response

        # If it cannot find the date then check for the Yesterday's
        self.date = datetime.today() - timedelta(days=1)
        return self.get_images()
