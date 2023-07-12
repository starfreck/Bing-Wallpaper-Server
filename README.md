# 🌄 Bing Wallpaper Server

A simple API Wrapper for [Bing Wallpaper](https://www.microsoft.com/en-us/bing/bing-wallpaper).

### 🚝 Run

- Create a .env file from .env.example above in the root folder.
- This app uses the MongoDB to store the already parsed image data.
- You might want to use a local or a remote version of MongoDB.
    
```shell
  pip3 install -r requirements.txt
  
  # Visit below link to see how to run a Flask app
  # https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application
```

## 📚 API Documentations

#### ⬅️ [GET] http://localhost:5000/

- This will give the  basic information about the application and the list of supported countries.

```json
{
    "app_name": "Bing-Wallpaper-Server",
    "default_country": "United States",
    "docs": "https://github.com/starfreck/Bing-Wallpaper-Server",
    "message": "Welcome to Bing Wallpaper APIs !!",
    "status": 1,
    "supported_countries": {
        "Australia": "au",
        "Canada": "ca",
        "China": "cn",
        "France": "fr",
        "Germany": "de",
        "India": "in",
        "Italy": "it",
        "Japan": "jp",
        "Spain": "es",
        "United Kingdom": "gb",
        "United States": "us"
    }
}
```
- The location parameter is an optional for all endpoints
- It will use "us" as a default location

#### ⬅️ [GET] http://localhost:5000/wallpaper?location=au

- Get the wallpaper of the day

#### ⬅️ [GET] http://localhost:5000/wallpaper/year/month/day?location=au

- Get the wallpaper of a specific date
- i.e. if you want to the wallpaper for 1st January 2023 then your request url should be as follows:

 ```
 http://localhost:5000/wallpaper/2023/01/01?location=au
```

## Credits
- [Peapix.com](https://peapix.com) for images
