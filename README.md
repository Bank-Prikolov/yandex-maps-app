# Yandex Maps App

![License](https://img.shields.io/github/license/dmhd6219/sdamgia-solver)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![Version](https://img.shields.io/badge/version-1.0-green)

Desktop application that includes [Yandex Maps API](https://yandex.ru/maps-api/) capabilities:
  * [Static API](https://yandex.com/maps-api/products/static-api?lang=en) for displaying a map
  * [Geocoder API](https://yandex.com/maps-api/products/geocoder-api?lang=en) for finding a place by request or mouse click
  * [Places API](https://yandex.com/maps-api/products/geosearch-api?lang=en) for finding the nearest organization by mouse click  

The app also supports several languages ​​and types of maps

> [!WARNING]
> The application was developed for educational purposes as part of training at [Yandex Lyceum](https://lyceum.yandex.ru/) and is not a Yandex product

## 📺 Preview
https://github.com/user-attachments/assets/857a00c6-6fc0-4b5a-a470-6cae08f68032

## 🛠️ Tech Stack
ㅤ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)
![Yandex Static API](https://img.shields.io/badge/yandex_static_api-FF0000?style=for-the-badge)
![Yandex Geocoder API](https://img.shields.io/badge/yandex_geocoder_api-FF0000?style=for-the-badge)
![Yandex Places API](https://img.shields.io/badge/yandex_places_api-FF0000?style=for-the-badge)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Aseprite](https://img.shields.io/badge/Aseprite-FFFFFF?style=for-the-badge&logo=Aseprite&logoColor=#7D929E)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

## 🎯 Quick Start
* Clone the project to your computer from Github using the command:
```
git clone https://github.com/mikhalexandr/yandex-maps-app.git
```

* Install all required dependencies from `requirements.txt`:
```
pip install requirements.txt
```

* Create `.env` in the root folder of the project:
```env
GEOCODER_API_KEY=your_geocoder_api_key
PLACES_API_KEY=your_places_api_key
```

* Run `app.py`

## 💾 Download App
* You can download `Yandex_Maps.zip` from [Release v1.0.0](https://github.com/mikhalexandr/yandex-maps-app/releases/tag/v1.0.0) and after unpacking the archive run `Yandex Maps.exe`
* You can download the project and create your own `.exe` file using the script from `create_exe.bat` in the terminal (you must be in the project folder and install all required dependencies)
