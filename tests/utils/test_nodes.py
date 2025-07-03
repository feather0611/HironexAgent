from agent.utils.nodes import geocode_node, weather_node
from agent.utils.state import AppState, create_app_state

def test_geocode_node_success_and_updates_state_correctly(mocker):
    initial_state: AppState = create_app_state("汐止區",{"google_map_api_key": "fake_google_key"})

    mock_tool_return_value = [{"display_name": "新北市汐止區", "lat": 25.06, "lon": 121.64}]

    mocker.patch(
        "agent.utils.nodes.get_geocode_of_location",
        return_value=mock_tool_return_value
    )

    updated_result = geocode_node(initial_state)

    assert isinstance(updated_result, dict)
    assert "geocode_locations" in updated_result
    assert updated_result["geocode_locations"] == mock_tool_return_value
    assert "error_message" not in updated_result

def test_geocode_node_handles_miss_apikey():
    initial_state: AppState = create_app_state("汐止", {})

    result_update = geocode_node(initial_state)

    assert isinstance(result_update, dict)
    assert "error_message" in result_update
    assert result_update["error_message"] is not None
    assert result_update["error_message"] == "Google Maps API Key is missing"
    assert "geocode_locations" not in result_update

def test_geocode_node_handles_tool_failure(mocker):
    initial_state: AppState = create_app_state("汐止", {"google_map_api_key": "wrong_google_key"})

    mocker.patch(
        "agent.utils.nodes.get_geocode_of_location",
        return_value=None
    )

    result_update = geocode_node(initial_state)

    assert isinstance(result_update, dict)
    assert "error_message" in result_update
    assert result_update["error_message"] is not None
    assert result_update["error_message"] == "Geocoding tool request failed, please check API key or network connection."
    assert "geocode_locations" not in result_update
    
def test_weather_node_success_and_updates_state_correctly(mocker):
    initial_state: AppState = create_app_state(
        user_input="台南",
        api_keys={"owm_api_key": "fake_owm_key"},
        geocode_locations=[
            {
                "formatted_address": "701台灣台南市東區",
                "geometry": {"location": {"lat": 22.980, "lng": 120.230}},
                "types": ["administrative_area_level_3", "political"]
            },
        ]
    )
    
    mock_tool_return_value = {
        "location": "Tainan City",
        "temperature": 29.5,
        "humidity": 75,
        "weather": "多雲"
    }
    
    mocker.patch(
        "agent.utils.nodes.get_weather_by_coords",
        return_value=mock_tool_return_value
    )
    
    updated_result = weather_node(initial_state)
    
    assert isinstance(updated_result, dict)
    