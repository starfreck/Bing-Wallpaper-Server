import datetime
from fastapi import FastAPI, Request
from ip_info import IPInfo
from bing_wallpaper import BingWallpaper

app = FastAPI()


@app.get("/")
async def root():
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


@app.get("/wallpaper")
async def get_today_s_wallpaper(request: Request):
    today = datetime.datetime.now()
    return get_wallpaper(request, today.year, today.month, today.day)


@app.get("/wallpaper/{year}/{month}/{day}")
async def get_wallpaper_from_date(request: Request, year: int, month: int, day: int):
    today = datetime.datetime.now()

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


def get_wallpaper(request: Request, year: int, month: int, day: int):
    ip = request.client.host
    ip_info = IPInfo().get_location(ip)
    bing = BingWallpaper(ip_info['country_name'], year, month, day)

    return {'status': 1, 'message': 'ok', 'ip_info': ip_info, 'date': str(year) + '/' + str(month) + '/' + str(day), 'wallpaper': bing.main()}


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
