import logging

from agent.utils.state import AppState

logger = logging.getLogger(__name__)

def route_after_geocoding(state: AppState) -> str:
    geocode_result = state.get("geocode_result")
    
    error_message = geocode_result.get("error_message")
    
    locations = geocode_result.get("result")
    
    if locations is None and error_message:
         return 'error'

    if len(locations) > 1:
        return 'ask_clarification'
    elif len(locations) == 0:
        return 'not_found'
    
    return 'get_weather'
    