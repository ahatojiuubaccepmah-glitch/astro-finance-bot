import requests


def geocode_city(city_name: str):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "astro-finance-bot"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()

    if not data:
        return None

    return {
        "lat": float(data[0]["lat"]),
        "lon": float(data[0]["lon"])
    }