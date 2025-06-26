import pytest
import requests
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

ZERO_RESULTS_RESPONSE = {
    "results": [],
    "status": "ZERO_RESULTS"
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
        pytest.param(
            "火山國", ZERO_RESULTS_RESPONSE, 0,
            id="case_zero_results_for_non_existent_place"
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

def test_get_geocode_of_location_handles_network_error(mocker):
    """
    GWT 場景四：當 API 請求因網路問題而失敗時，函式應回傳 None。
    """
    # 假設 (Given):
    # 我們設定 mocker，讓 requests.get 在被呼叫時，直接拋出一個網路錯誤
    mocker.patch(
        "agent.utils.tools.weather_tools.requests.get",
        side_effect=requests.exceptions.RequestException("Simulated network error")
    )

    # 當 (When):
    # 使用任何地點名稱呼叫函式
    result = get_geocode_of_location("任何地點", "fake_google_api_key")

    # 那麼 (Then):
    # 我們應該會收到 None
    assert result is None