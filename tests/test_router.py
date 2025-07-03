import pytest
from agent.router import route_after_geocoding
from agent.utils.state import AppState, create_app_state


@pytest.mark.parametrize(
    "current_state, expected_route",
    [
        pytest.param(
            {"geocode_locations": [{"name": "地點A"}]},
            "get_weather",
            id="route_to_get_weather_when_one_choice"
        ),

        pytest.param(
            {"geocode_locations": [{"name": "地點A"}, {"name": "地點B"}]},
            "ask_clarification",
            id="route_to_ask_clarification_when_multiple_choices"
        ),

        pytest.param(
            {"geocode_locations": []},
            "not_found",
            id="route_to_not_found_when_choices_is_empty"
        ),

        pytest.param(
            {"error_message": "An error occurred"},
            "error",
            id="route_to_error_when_error_message_exists"
        ),
    ]
)
def test_route_after_geocoding(current_state, expected_route):
    error_message = current_state.get("error_message")

    state: AppState = create_app_state("any", {}, geocode_locations=current_state.get("geocode_locations"), error_message=error_message)

    next_node = route_after_geocoding(state)

    assert next_node == expected_route