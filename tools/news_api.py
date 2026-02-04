import os
import requests

class NewsAPITool:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        if not self.api_key:
            raise RuntimeError("Missing NEWS_API_KEY in environment variables.")
        self.base_url = "https://newsapi.org/v2/"

    def search_news(self, query: str, count: int = 5) -> list:
        url = self.base_url + "everything"
        params = {
            "q": query,
            "pageSize": count,
            "sortBy": "relevancy",
            "language": "en",
            "apiKey": self.api_key,
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise RuntimeError(f"NewsAPI error: {response.text}")
        articles = response.json().get("articles", [])
        return [a.get("title") for a in articles if a.get("title")]

    def get_top_headlines(self, country: str = "us", category: str = None, count: int = 5) -> list:
        url = self.base_url + "top-headlines"
        params = {
            "country": country,
            "pageSize": count,
            "apiKey": self.api_key,
        }
        if category:
            params["category"] = category
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise RuntimeError(f"NewsAPI error: {response.text}")
        articles = response.json().get("articles", [])
        return [a.get("title") for a in articles if a.get("title")]
