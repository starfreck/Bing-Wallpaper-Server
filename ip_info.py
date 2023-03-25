import os
import json
import requests
from dotenv import load_dotenv

GEO_LOCATION_DB_URL = os.getenv('GEO_LOCATION_DB_URL')

def get_location(ip_address):
    # URL to send the request to
    request_url = f'{GEO_LOCATION_DB_URL}/{ip_address}'
    # Send request and decode the result
    response = requests.get(request_url)
    result = response.content.decode()
    # Clean the returned string so it just contains the dictionary data for the IP address
    result = result.split("(")[1].strip(")")
    # Convert this data into a dictionary
    return json.loads(result)
