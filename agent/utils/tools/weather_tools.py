import requests

def get_geocode_of_location(location_name: str, api_key: str) -> list | None:

    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": f"{location_name}+tw",
        "key": api_key,
        "language": "zh-TW",
        "result_type": "administrative_area_level_1|administrative_area_level_2|administrative_area_level_3"
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "OK" and data.get("results"):
            api_results = data.get("results", [])

            valid_results = [
                result for result in api_results
                if (
                    location_name in result.get("formatted_address", "")
                )
            ]
            return valid_results
        else:
            return []

    except requests.exceptions.RequestException as e:
        print(f"Geocoding API Request Failed: {e}")
        return None