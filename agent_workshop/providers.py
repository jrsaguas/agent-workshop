from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol
import json
from urllib.request import Request, urlopen

class ModelProvider(Protocol):
    def generate(self, model: str, prompt: str, **options: Any) -> str: ...

@dataclass
class OllamaProvider:
    base_url: str = "http://127.0.0.1:11434"
    timeout: float = 120.0

    def generate(self, model: str, prompt: str, **options: Any) -> str:
        payload = json.dumps({"model": model, "prompt": prompt, "stream": False, **options}).encode()
        request = Request(f"{self.base_url}/api/generate", data=payload, headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=self.timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data.get("response", "")

class ProviderRegistry:
    def __init__(self, providers: dict[str, ModelProvider] | None = None):
        self._providers = providers or {"ollama": OllamaProvider()}

    def get(self, provider: str) -> ModelProvider:
        try:
            return self._providers[provider]
        except KeyError as exc:
            raise KeyError(f"provider not configured: {provider}") from exc
