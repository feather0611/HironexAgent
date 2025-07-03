from typing import TypedDict, List, Dict, Any, Optional

class AppState(TypedDict):
    user_input: str
    api_keys: Dict[str, str]
    geocode_locations: Optional[List[Dict[str, Any]]]
    weather: Optional[Dict[str, Any]]
    final_answer: Optional[str]
    error_message: Optional[str]

def create_app_state(
    user_input: str,
    api_keys: Dict[str, str],
    geocode_locations: Optional[List[Dict[str, Any]]]=None,
    weather: Optional[Dict[str, Any]]=None,
    final_answer: Optional[str]=None,
    error_message: Optional[str]=None,
) -> AppState:
    return {
        "user_input": user_input,
        "api_keys": api_keys,
        "geocode_locations": geocode_locations,
        "weather": weather,
        "final_answer": final_answer,
        "error_message": error_message
    }