import pytest
from agent.utils.tools.weather_tools import get_geocode_of_location

SINGLE_LOCATION_RESPONSE = {
    "results": [
        {
            "formatted_address": "221台灣新北市汐止區",
            "geometry": {"location": {"lat": 25.067, "lng": 121.644}},
            "types": ["administrative_area_level_3", "political"]
        }
    ],
    "status": "OK"
}

MULTIPLE_LOCATIONS_RESPONSE = {
    "results": [
        {
            "formatted_address": "300台灣新竹市東區",
            "geometry": {"location": {"lat": 24.804, "lng": 120.973}},
            "types": ["administrative_area_level_3", "political"]
        },
        {
            "formatted_address": "600台灣嘉義市東區",
            "geometry": {"location": {"lat": 23.478, "lng": 120.453}},
            "types": ["administrative_area_level_3", "political"]
        },
        {
            "formatted_address": "701台灣台南市東區",
            "geometry": {"location": {"lat": 22.980, "lng": 120.230}},
            "types": ["administrative_area_level_3", "political"]
        }
    ],
    "status": "OK"
}

def setup_mock_api(mocker, status_code, json_response):
    mock_response = mocker.Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_response
    mocker.patch("agent.utils.tools.weather_tools.requests.get", return_value=mock_response)

@pytest.mark.parametrize(
    "location_name, api_response, expected_count",
    [
        pytest.param(
            "汐止", SINGLE_LOCATION_RESPONSE, 1,
            id="case_single_result_for_Xizhi"
        ),
        pytest.param(
            "東區", MULTIPLE_LOCATIONS_RESPONSE, 3,
            id="case_multiple_results_for_East_District"
        ),
    ]
)
def test_get_geocode_of_location(mocker, location_name, api_response, expected_count):
    setup_mock_api(mocker, status_code=200, json_response=api_response)

    locations = get_geocode_of_location(location_name, 'fake_google_api_key')

    assert locations is not None
    assert isinstance(locations, list)
    assert len(locations) == expected_count

    for location_data in locations:
        assert location_name in location_data["formatted_address"]
        assert "lat" in location_data["geometry"]["location"]
        assert "lng" in location_data["geometry"]["location"]