import os
import requests

class LLMClient:
    def __init__(self, model="mistralai/mistral-7b-instruct", api_key=None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        if not self.api_key:
            raise RuntimeError("Missing OPENROUTER_API_KEY.")

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        response = requests.post(self.base_url, headers=headers, json=data)
        if response.status_code != 200:
            raise RuntimeError(f"OpenRouter Error: {response.text}")
        return response.json()["choices"][0]["message"]["content"]
