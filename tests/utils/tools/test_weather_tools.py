import pytest
import requests
from agent.utils.tools.weather_tools import get_geocode_of_location, get_weather_by_coords

GEOCODE_SINGLE_LOCATION_RESPONSE = {
    "results": [
        {
            "formatted_address": "221台灣新北市汐止區",
            "geometry": {"location": {"lat": 25.067, "lng": 121.644}},
            "types": ["administrative_area_level_3", "political"]
        }
    ],
    "status": "OK"
}

GEOCODE_MULTIPLE_LOCATIONS_RESPONSE = {
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

GEOCODE_ZERO_RESULTS_RESPONSE = {
    "results": [],
    "status": "ZERO_RESULTS"
}

def setup_mock_api_response(mocker, status_code, json_response):
    mock_response = mocker.Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_response
    if status_code >= 400:
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(f"{status_code} Error")
    mocker.patch("agent.utils.tools.weather_tools.requests.get", return_value=mock_response)

@pytest.mark.parametrize(
    "location_name, api_response, expected_count",
    [
        pytest.param(
            "汐止", GEOCODE_SINGLE_LOCATION_RESPONSE, 1,
            id="case_single_result_for_Xizhi"
        ),
        pytest.param(
            "東區", GEOCODE_MULTIPLE_LOCATIONS_RESPONSE, 3,
            id="case_multiple_results_for_East_District"
        ),
        pytest.param(
            "火山國", GEOCODE_ZERO_RESULTS_RESPONSE, 0,
            id="case_zero_results_for_non_existent_place"
        ),
    ]
)
def test_get_geocode_of_location(mocker, location_name, api_response, expected_count):
    setup_mock_api_response(mocker, status_code=200, json_response=api_response)

    locations = get_geocode_of_location(location_name, 'fake_google_api_key')

    assert locations is not None
    assert isinstance(locations, list)
    assert len(locations) == expected_count

    for location_data in locations:
        assert location_name in location_data["formatted_address"]
        assert "lat" in location_data["geometry"]["location"]
        assert "lng" in location_data["geometry"]["location"]

def test_get_geocode_of_location_handles_network_error(mocker):
    mocker.patch(
        "agent.utils.tools.weather_tools.requests.get",
        side_effect=requests.exceptions.RequestException("Simulated network error")
    )

    result = get_geocode_of_location("任何地點", "fake_google_api_key")

    assert result is None

def test_get_weather_by_coords_success(mocker):
    mock_api_response = {
        "weather": [{
            "main": "Clouds",
            "description": "多雲",
        }],
        "main": {
            "temp": 29.5,
            "feels_like": 33.22,
            "temp_min": 29.73,
            "temp_max": 29.73,
            "humidity": 75,
        },
        "name": "Tainan City"
    }

    setup_mock_api_response(mocker, 200, mock_api_response)
    
    result = get_weather_by_coords(22.980, 120.230, "fake_owm_api_key")

    assert isinstance(result, dict)
    assert result["location"] == "Tainan City"
    assert result["temperature"] == 29.5
    assert result["humidity"] == 75
    assert result["weather"] == "多雲"

def test_get_weather_by_coords_unauthorized(mocker):
    mock_api_response = {
        "cod": 401,
        "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."
    }
    
    setup_mock_api_response(mocker, status_code=401, json_response=mock_api_response)

    result = get_weather_by_coords(22.980, 120.230, "invalid_api_key")

    assert result is None

def test_get_weather_by_coords_network_error(mocker):
    mocker.patch(
        "agent.utils.tools.weather_tools.requests.get",
        side_effect=requests.exceptions.RequestException("Simulated network connection error")
    )

    result = get_weather_by_coords(22.980, 120.230, "any_api_key")

    assert result is None

def test_get_weather_by_coords_handles_malformed_data(mocker):
    mock_api_response = {
        "weather": [{"description": "晴時多雲"}],
        "name": "Taipei"
    }

    setup_mock_api_response(mocker, status_code=200, json_response=mock_api_response)
    
    result = get_weather_by_coords(25.033, 121.5654, "fake_owm_api_key")

    assert isinstance(result, dict)

    assert result["location"] == "Taipei"
    assert result["weather"] == "晴時多雲"

    assert result["temperature"] is None
    assert result["humidity"] is None