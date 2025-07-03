from .state import AppState
from .tools.weather_tools import get_geocode_of_location

import logging

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
