# 🌄 Bing Wallpaper Server

A simple API Wrapper for [Bing Wallpaper](https://www.microsoft.com/en-us/bing/bing-wallpaper).

### 🚝 Run

- Create a .env file from .env.example above in the root folder.
- This app uses the MongoDB to store the alredy parsed image date you might want to use a local or a remove version of MongoDB.
    
    `pip3 install -r requirements.txt`  
    `python3 app.py`

## 📚 API Documentations

#### ⬅️ [GET] http://localhost:5000/

- This will give the  basic information about the application and the supported countries.

#### ⬅️ [GET] http://localhost:5000/wallpaper

- Get the wallpaper of the day

#### ⬅️ [GET] http://localhost:5000/wallpaper/year/month/day

- Get the wallpaper of a specific date i.e. if you want to the wallpaper for 1st January 2023 then your request url should be as follows:

    `
    http://localhost:5000/wallpaper/2023/01/01
    `

## Credits
- [Peapix.com](https://peapix.com) for images
