import logging

from .state import AppState
from .tools.weather_tools import get_geocode_of_location, get_weather_by_coords

logger = logging.getLogger(__name__)

def geocode_node(state: AppState) -> dict:
    logger.info("--- Run node: geocode_node ---")

    user_input = state["user_input"]
    api_key = state["api_keys"].get("google_map_api_key")

    if not api_key:
        return {"error_message": "Google Maps API Key is missing"}

    results = get_geocode_of_location(user_input, api_key)

    if results is None:
        return {"error_message": "Geocoding tool request failed, please check API key or network connection."}

    logger.info(f"    -> Geocoding tool found {len(results)} of possible locations")
    return {"geocode_locations": results}


def weather_node(state: AppState) -> dict:
    owm_api_key = state["api_keys"].get("owm_api_key")
    geocode_locations = state["geocode_locations"]
    if not owm_api_key:
        return {"error_message": "OWM API Key is missing"}
    if not geocode_locations or len(geocode_locations) == 0:
        return {"error_message": "Geocode is not set"}
    if len(geocode_locations) > 1:
        return {"error_message": "Query more than one location"}
    query = geocode_locations[0].get("geometry").get("location")
    if not query:
        return {"error_message": "Can't find location in geocode response"}
    result = get_weather_by_coords(query["lat"], query["lng"], owm_api_key)
    
    if result is None:
        return {"error_message": "weather query failed, please check API key or network connection."}
    
    return {"weather": result}
    