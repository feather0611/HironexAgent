import logging

from .state import AppState
from .tools.weather_tools import get_geocode_of_location, get_weather_by_coords

logger = logging.getLogger(__name__)

def geocode_node(state: AppState) -> dict:

    user_input = state["user_input"]
    api_key = state["api_keys"].get("google_map_api_key")

    if not api_key:
        return {
            "geocode_result": {
                "pass_status": False, 
                "error_message": "Google Maps API Key is missing"
            }
        }

    results = get_geocode_of_location(user_input, api_key)

    if results is None:
        return {
            "geocode_result":{
                "pass_status": False, 
                "error_message": "Geocoding tool request failed, please check API key or network connection."
            }
        }

    logger.debug(f"Geocoding tool found {len(results)} of possible locations")
    return {
        "geocode_result": {
            "pass_status": True, 
            "result": results
        }
    }


def weather_node(state: AppState) -> dict:
    owm_api_key = state["api_keys"].get("owm_api_key")
    if not owm_api_key:
        return {
            "weather_result": {
                "pass_status": False, 
                "error_message": "OWM API Key is missing"
            }
        }
    
    geocode_locations = state["geocode_result"].get("result")
    if not geocode_locations or len(geocode_locations) == 0:
        return {
            "weather_result": {
                "pass_status": False, 
                "error_message": "Geocode is not set"
            }
        }
    
    if len(geocode_locations) > 1:
        return {
            "weather_result": {
                "pass_status": False, 
                "error_message": "Query more than one location"
            }
        }
    
    query = geocode_locations[0]
    if not query:
        return {
            "weather_result": {
                "pass_status": False, 
                "error_message": "Can't find geocode in location"
            }
        }
    
    result = get_weather_by_coords(query["lat"], query["lon"], owm_api_key)
    
    if result is None:
        return {
            "weather_result": {
                "pass_status": False, 
                "error_message": "Weather query failed, please check API key or network connection."
            }
        }
    
    return {
        "weather_result": {
            "pass_status": True,
            "result": result
        }
    }
    