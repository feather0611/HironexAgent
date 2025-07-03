from agent.utils.state import AppState

def route_after_geocoding(state: AppState) -> str:
    locations = state.get("geocode_locations")
    error_message = state.get("error_message")
    
    if locations is None and error_message:
         return 'error'
    
    count_of_locations = len(locations)
    
    if count_of_locations > 1:
        return 'ask_clarification'
    elif count_of_locations == 0:
        return 'not_found'
    
    return 'get_weather'
    