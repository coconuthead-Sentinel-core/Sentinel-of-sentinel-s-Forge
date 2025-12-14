import os
import requests
from typing import Optional, Dict, Any, Union


class SentinelClient:
    """
    Official Python Client for Sentinel Forge API.
    Features:
    - Automatic session management (connection pooling)
    - Default timeouts
    - Environment variable support
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 10):
        self.base_url = (base_url or os.getenv("API_BASE_URL", "http://127.0.0.1:8000")).rstrip("/")
        self.api_key = api_key or os.getenv("API_KEY")
        self.timeout = timeout

        # Use a session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        if self.api_key:
            self.session.headers.update({"X-API-Key": self.api_key})

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/api{endpoint}"
        try:
            resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.JSONDecodeError:
            return {"error": "Invalid JSON response", "text": resp.text}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def status(self) -> Dict[str, Any]:
        """Check system status."""
        return self._request("GET", "/status")

    def chat(self, message: str, context: str = "") -> str:
        """Send a chat message to the AI."""
        payload = {
            "messages": [
                {"role": "system", "content": context},
                {"role": "user", "content": message},
            ]
        }
        data = self._request("POST", "/ai/chat", json=payload)
        # Safe extraction
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, TypeError, IndexError):
            return data.get("error", "No response content")

    def upsert_note(self, text: str, tag: str) -> Dict[str, Any]:
        """Save a note to the memory lattice (Cosmos DB)."""
        return self._request("POST", "/notes/upsert", json={"text": text, "tag": tag})

    def run_cognition(self, data: str) -> Dict[str, Any]:
        """Run the cognitive processing pipeline."""
        return self._request("POST", "/cog/process", json={"data": data})


# Example Usage
if __name__ == "__main__":
    client = SentinelClient()
    print("Checking Status...", client.status())
