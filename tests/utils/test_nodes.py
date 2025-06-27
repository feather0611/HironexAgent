from agent.utils.nodes import geocode_node
from agent.utils.state import AppState

def test_geocode_node_success_and_updates_state_correctly(mocker):
    initial_state: AppState = {
        "user_input": "汐止區",
        "api_keys": {"google_map_api_key": "fake_google_key"},
        "choices": None,
        "final_answer": None,
        "error_message": None
    }

    mock_tool_return_value = [{"display_name": "新北市汐止區", "lat": 25.06, "lon": 121.64}]

    mocker.patch(
        "agent.utils.nodes.get_geocode_of_location",
        return_value=mock_tool_return_value
    )

    result_update = geocode_node(initial_state)

    assert isinstance(result_update, dict)
    assert "choices" in result_update
    assert result_update["choices"] == mock_tool_return_value
    assert "error_message" not in result_update

def test_geocode_node_handles_miss_apikey():
    initial_state: AppState = {
        "user_input": "汐止",
        "api_keys": {},
        "choices": None,
        "final_answer": None,
        "error_message": None
    }

    result_update = geocode_node(initial_state)

    assert isinstance(result_update, dict)
    assert "error_message" in result_update
    assert result_update["error_message"] is not None
    assert result_update["error_message"] == "Google Maps API Key is missing"
    assert "choices" not in result_update

def test_geocode_node_handles_tool_failure(mocker):
    initial_state: AppState = {
        "user_input": "汐止",
        "api_keys": {"google_map_api_key": "wrong_google_key"},
        "choices": None,
        "final_answer": None,
        "error_message": None
    }

    mocker.patch(
        "agent.utils.nodes.get_geocode_of_location",
        return_value=None
    )

    result_update = geocode_node(initial_state)

    assert isinstance(result_update, dict)
    assert "error_message" in result_update
    assert result_update["error_message"] is not None
    assert result_update["error_message"] == "Geocoding tool request failed, please check API key or network connection."
    assert "choices" not in result_update