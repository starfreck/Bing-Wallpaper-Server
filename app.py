import datetime

from flask import Flask, request
from flask_pymongo import PyMongo

from ip_info import get_location
from bing_wallpaper import BingWallpaper
from db import get_db_conn_str as db_string

app = Flask(__name__)
app.config["MONGO_URI"] = db_string()

mongo = PyMongo(app)


@app.route('/', methods=['GET'])
def root():
    return {
        "status": 1,
        "app_name": "Bing-Wallpaper-Server",
        "message": "Countries are automatically selected by the IP address...",
        "default_country": "United States",
        "supported_countries": [
            "Australia",
            "Canada",
            "China",
            "Germany",
            "France",
            "India",
            "Japan",
            "Spain",
            "United Kingdom",
            "United States",
            "Italy"
        ]
    }


@app.route('/wallpaper', methods=['GET'])
def get_today_s_wallpaper():
    today = datetime.datetime.now()
    return get_wallpaper(request, today.year, today.month, today.day)


@app.route('/wallpaper/<year>/<month>/<day>', methods=['GET'])
def get_wallpaper_from_date(year, month, day):
    day = int(day)
    month = int(month)
    year = int(year)

    if year < 2010:
        return {'status': 0, 'message': 'Invalid Year! Only the period from 2010 onward is supported!'}
    elif month < 0 or month > 12:
        return {'status': 0, 'message': 'Invalid Month!'}
    elif day < 1 or day > 31:
        return {'status': 0, 'message': 'Invalid Day!'}
    elif not is_valid_date(year, month, day):
        return {'status': 0, 'message': 'Invalid Date!'}
    elif is_future_date(year, month, day):
        return {'status': 0, 'message': 'Future Date!'}
    else:
        return get_wallpaper(request, year, month, day)


def get_wallpaper(request: request, year: int, month: int, day: int):
    
    ip = request.remote_addr
    ip_info = get_location(ip)

    bing = BingWallpaper(mongo.db.bing_store, ip_info['country_name'], year, month, day)
    return {
        'status': 1,
        'message': 'ok',
        'ip_info': ip_info,
        'date': f'{str(year)}/{str(month)}/{str(day)}',
        'wallpaper': bing.get_images()
    }


def is_valid_date(year: int, month: int, day: int):
    flag = True
    try:
        datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        flag = False
    return flag


def is_future_date(year: int, month: int, day: int):
    today = datetime.datetime.now()
    date = None
    try:
        date = datetime.datetime(int(year), int(month), int(day))
    except ValueError:
        print("Exception occurred!")
    if date <= today:
        return False
    return True
