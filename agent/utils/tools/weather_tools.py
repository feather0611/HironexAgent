import requests
import logging

logger = logging.getLogger(__name__)

def _api_request(base_url, params):
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.exception(f"API Request Failed: {e}")
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
        return None

    if data.get("status") == "OK" and data.get("results"):
        return data["results"]
    else:
        return []


def get_weather_by_coords(lat: float, lon: float, api_key:str) -> dict | None:
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": f"{lat}",
        "lon": f"{lon}",
        "appid": api_key,
        "lang": "zh_tw",
        "units": "metric"
    }

    data = _api_request(base_url, params)
    
    if data is None:
        return None
    
    try:
        main_data = data.get("main", {})
        weather_list = data.get("weather", [])
        return {
            "location": data.get("name"),
            "temperature": main_data.get("temp"),
            "humidity": main_data.get("humidity"),
            "weather": weather_list[0].get("description") if weather_list else None,
        }
    except (KeyError, IndexError) as e:
        logger.exception(f"Error when parsing data: {e}")
        return None
    