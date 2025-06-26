import requests


def _api_request(base_url, params):
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Request Failed: {e}")
        return None 


def get_geocode_of_location(location_name: str, api_key: str) -> list | None:

    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": f"{location_name}+tw",
        "key": api_key,
        "language": "zh-TW",
        "result_type": "administrative_area_level_1|administrative_area_level_2|administrative_area_level_3"
    }

    data = _api_request(base_url, params)
    
    if data is None:
        return None  # 表示網路層級或 HTTP 錯誤

    if data.get("status") == "OK" and data.get("results"):
        return data["results"]
    else:
        return []


def get_weather_by_coords(lat: float, lng: float, api_key:str):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": f"{lat}",
        "lon": f"{lng}",
        "appid": api_key,
        "lang": "zh_tw",
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        main_data = data.get("main", {})
        temp = main_data.get("temp")
        humidity = main_data.get("humidity")

        weather_list = data.get("weather", [])
        weather_description = weather_list[0].get("description") if weather_list else None

        location = data.get("name")

        result = {
            "location": location,
            "temperature": temp,
            "humidity": humidity,
            "weather": weather_description,
        }
        return result

    except requests.exceptions.RequestException as e:
        print(f"Weather API Request Failed: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error when parsing data: {e}")
        return None
    