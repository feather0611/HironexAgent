from agent.utils.nodes import geocode_node, weather_node
from agent.utils.state import AppState, create_app_state, create_tool_result


def test_geocode_node_success_and_updates_state_correctly(mocker):
    initial_state: AppState = create_app_state("請告訴我汐止的天氣",{"google_map_api_key": "fake_google_key"}, "汐止")

    mock_tool_return_value = [{"display_name": "新北市汐止區", "lat": 25.06, "lon": 121.64}]

    mocker.patch(
        "agent.utils.nodes.get_geocode_of_location",
        return_value=mock_tool_return_value
    )

    updated_state = geocode_node(initial_state)

    assert isinstance(updated_state, dict)
    assert "geocode_result" in updated_state

    geocode_result = updated_state["geocode_result"]
    assert isinstance(geocode_result, dict)
    
    assert geocode_result["pass_status"] == True
    assert geocode_result["result"] == mock_tool_return_value
    assert "error_message" not in geocode_result

def test_geocode_node_handles_miss_apikey():
    initial_state: AppState = create_app_state("請告訴我汐止的天氣", {}, "汐止")

    updated_state = geocode_node(initial_state)

    assert isinstance(updated_state, dict)
    assert "geocode_result" in updated_state
    
    geocode_result = updated_state["geocode_result"]
    assert isinstance(geocode_result, dict)
    
    assert geocode_result["pass_status"] == False
    assert "error_message" in geocode_result
    assert geocode_result["error_message"] is not None
    assert geocode_result["error_message"] == "Google Maps API Key is missing"
    assert "result" not in geocode_result

def test_geocode_node_handles_tool_failure(mocker):
    initial_state: AppState = create_app_state("汐止天氣如何", {"google_map_api_key": "wrong_google_key"}, "汐止")

    mocker.patch(
        "agent.utils.nodes.get_geocode_of_location",
        return_value=None
    )

    updated_state = geocode_node(initial_state)

    assert isinstance(updated_state, dict)
    assert "geocode_result" in updated_state
    
    geocode_result = updated_state["geocode_result"]
    assert isinstance(geocode_result, dict)
    
    assert geocode_result["pass_status"] == False
    assert "error_message" in geocode_result
    assert geocode_result["error_message"] is not None
    assert geocode_result["error_message"] == "Geocoding tool request failed, please check API key or network connection."
    assert "result" not in geocode_result
    
def test_geocode_node_handles_no_query_location():
    initial_state: AppState = create_app_state("你是誰啊？", {"google_map_api_key": "fake_google_key"})
    
    updated_state = geocode_node(initial_state)
    
    assert isinstance(updated_state, dict)
    assert "geocode_result" in updated_state
    
    geocode_result = updated_state["geocode_result"]
    assert isinstance(geocode_result, dict)
    assert geocode_result["pass_status"] == False
    assert "error_message" in geocode_result
    assert geocode_result["error_message"] is not None
    assert geocode_result["error_message"] == "Can't get any location to search"
    assert "result" not in geocode_result
    
def test_weather_node_success_and_updates_state_correctly(mocker):
    mock_geocode_result = create_tool_result(True, [
        {
            "formatted_address": "701台灣台南市東區",
            "lat": 22.980, 
            "lon": 120.230
        }
    ])
    
    initial_state: AppState = create_app_state(
        user_input="台南的天氣如何？",
        api_keys={"owm_api_key": "fake_owm_key"},
        query_location="台南",
        geocode_result=mock_geocode_result
    )
    
    mock_tool_return_value = {
        "temperature": 29.5,
        "humidity": 75,
        "weather": "多雲"
    }
    
    mocker.patch(
        "agent.utils.nodes.get_weather_by_coords",
        return_value=mock_tool_return_value
    )
    
    updated_state = weather_node(initial_state)
    
    assert isinstance(updated_state, dict)
    assert "weather_result" in updated_state
    
    weather_result = updated_state["weather_result"]
    assert isinstance(weather_result, dict)
    
    assert weather_result["pass_status"] == True
    assert weather_result["result"] == mock_tool_return_value
    assert "error_message" not in weather_result
    
def test_weather_node_handles_miss_apikey():
    initial_state: AppState = create_app_state("汐止", {})
    
    updated_state = weather_node(initial_state)
    
    assert isinstance(updated_state, dict)
    assert "weather_result" in updated_state
    
    weather_result = updated_state["weather_result"]
    assert isinstance(weather_result, dict)
    
    assert "error_message" in weather_result
    assert weather_result["error_message"] is not None
    assert weather_result["error_message"] == "OWM API Key is missing"
    assert "result" not in weather_result
    
    