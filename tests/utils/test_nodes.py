from agent.utils.nodes import geocode_node
from agent.utils.state import AppState

def test_geocode_node_success_and_updates_state_correctly(mocker):
    initial_state: AppState = {
        "user_input": "汐止區",
        "api_keys": {"google": "fake_google_key"},
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