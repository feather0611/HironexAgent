from agent.utils.tools.weather_tools import get_geocode_of_location

def test_get_geocode_of_location_single_valid_result(mocker):
    mock_api_response = {
        "results": [
            {
                "formatted_address": "221台灣新北市汐止區",
                "geometry": { "location": { "lat": 25.067, "lng": 121.644 } },
                "types": ["administrative_area_level_3", "political"]
            }
        ],
        "status": "OK"
    }

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_api_response
    mocker.patch("agent.utils.tools.weather_tools.requests.get", return_value=mock_response)

    result = get_geocode_of_location('', '')

    assert isinstance(result, list)
    assert len(result) == 1

    first_result = result[0]

    assert "汐止" in first_result["formatted_address"]
    assert "lat" in first_result["geometry"]["location"]
    assert "lng" in first_result["geometry"]["location"]

def test_get_geocode_of_location_ambiguous_returns_multiple(mocker):
    mock_api_response = {
        "results": [
            {
                "formatted_address": "300台灣新竹市東區",
                "geometry": { "location": { "lat": 24.804, "lng": 120.973 } },
                "types": ["administrative_area_level_3", "political"]
            },
            {
                "formatted_address": "600台灣嘉義市東區",
                "geometry": { "location": { "lat": 23.478, "lng": 120.453 } },
                "types": ["administrative_area_level_3", "political"]
            },
            {
                "formatted_address": "701台灣台南市東區",
                "geometry": { "location": { "lat": 22.980, "lng": 120.230 } },
                "types": ["administrative_area_level_3", "political"]
            }
        ],
        "status": "OK"
    }

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_api_response
    mocker.patch("agent.utils.tools.weather_tools.requests.get", return_value=mock_response)

    result = get_geocode_of_location("東區", "fake_google_api_key")

    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 3

    for item in result:
        assert "東區" in item["formatted_address"]
        assert "lat" in item["geometry"]["location"]
        assert "lng" in item["geometry"]["location"]