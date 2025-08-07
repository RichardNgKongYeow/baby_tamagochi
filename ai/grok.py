import requests
import os
from dotenv import load_dotenv


class GrokInterface:
    def __init__(self, api_key):
        """Initialize the Grok interface with default settings."""
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.model = "grok-3"  # Placeholder model name
        self.api_url = "https://api.xai.com/v1/chat"  # Placeholder URL, replace with actual endpoint

    def send_message(self, prompt: str) -> str:
        """Send a message to Grok and return the response."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "max_tokens": 150,
                "temperature": 0.7
            }
            response = requests.post(self.api_url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            return f"Error interacting with Grok: {str(e)}"

    def set_model(self, model_name: str):
        """Set the Grok model to use."""
        self.model = model_name

    def set_api_url(self, url: str):
        """Set the Grok API URL (for flexibility if endpoint changes)."""
        self.api_url = url