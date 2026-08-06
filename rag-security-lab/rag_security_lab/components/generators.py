from __future__ import annotations

import os
from typing import Any

import requests

from ..registry import GENERATORS


class _HttpGenerator:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.base_url = str(config.get("base_url", "http://localhost:11434")).rstrip("/")
        self.model = str(config.get("model", "qwen3:8b"))
        self.temperature = float(config.get("temperature", 0.0))
        self.timeout = int(config.get("timeout", 300))


@GENERATORS.register("ollama")
class OllamaGenerator(_HttpGenerator):
    def generate(self, prompt: str) -> str:
        response = requests.post(
            self.base_url + "/api/chat",
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": self.temperature},
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]


@GENERATORS.register("openai_compatible")
class OpenAICompatibleGenerator(_HttpGenerator):
    def generate(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        env_name = str(self.config.get("api_key_env", "OPENAI_API_KEY"))
        api_key = os.environ.get(env_name)
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        response = requests.post(
            self.base_url + "/chat/completions",
            headers=headers,
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": self.temperature,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

