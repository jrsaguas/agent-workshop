from agent_workshop.providers import ProviderRegistry

def test_ollama_provider_is_registered():
    provider = ProviderRegistry().get("ollama")
    assert provider.__class__.__name__ == "OllamaProvider"
