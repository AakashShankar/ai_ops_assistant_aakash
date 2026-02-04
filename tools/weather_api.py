import os
import requests

class OpenWeatherTool:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise RuntimeError("Missing OPENWEATHER_API_KEY.")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_current_weather(self, city: str) -> dict:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        resp = requests.get(self.base_url, params=params)
        if resp.status_code != 200:
            raise RuntimeError(f"OpenWeather API error: {resp.text}")
        data = resp.json()
        return {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature": data.get("main", {}).get("temp"),
            "humidity": data.get("main", {}).get("humidity"),
            "description": data.get("weather", [{}])[0].get("description")
        }
