from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

class ProviderError(RuntimeError):
    """Base error for model-provider failures."""


class ProviderConnectionError(ProviderError):
    pass


class ProviderTimeoutError(ProviderConnectionError):
    pass


class ProviderResponseError(ProviderError):
    pass


class ModelProvider(Protocol):
    def generate(self, model: str, prompt: str, **options: Any) -> str: ...

@dataclass
class OllamaProvider:
    base_url: str = "http://127.0.0.1:11434"
    timeout: float = 120.0
    connect_timeout: float | None = None

    def health(self) -> bool:
        """Return whether the Ollama API is reachable."""
        request = Request(f"{self.base_url}/api/tags", method="GET")
        try:
            with urlopen(request, timeout=self.connect_timeout or 5.0) as response:
                return 200 <= response.status < 300
        except (TimeoutError, URLError, HTTPError):
            return False

    def generate(self, model: str, prompt: str, **options: Any) -> str:
        payload = json.dumps({"model": model, "prompt": prompt, "stream": False, **options}).encode()
        request = Request(f"{self.base_url}/api/generate", data=payload, headers={"Content-Type": "application/json"})
        timeout = self.connect_timeout if self.connect_timeout is not None else self.timeout
        try:
            with urlopen(request, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except TimeoutError as exc:
            raise ProviderTimeoutError(f"provider request timed out after {timeout}s") from exc
        except (URLError, HTTPError) as exc:
            raise ProviderConnectionError(f"provider connection failed: {exc}") from exc
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ProviderResponseError("provider returned invalid JSON") from exc
        if not isinstance(data, dict):
            raise ProviderResponseError("provider returned a non-object response")
        return data.get("response", "")

class ProviderRegistry:
    def __init__(self, providers: dict[str, ModelProvider] | None = None):
        self._providers = providers or {"ollama": OllamaProvider()}

    def get(self, provider: str) -> ModelProvider:
        try:
            return self._providers[provider]
        except KeyError as exc:
            raise KeyError(f"provider not configured: {provider}") from exc
