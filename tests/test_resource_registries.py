from pathlib import Path
from agent_workshop.resource_registries import ModelRegistry, ToolRegistry, MCPRegistry

def test_resource_registries_load_examples():
    root = Path(__file__).parents[1]
    models = ModelRegistry(root / "models").list()
    tools = ToolRegistry(root / "tools").list()
    mcps = MCPRegistry(root / "mcp").list()
    qwen = next(model for model in models if model.id == "ollama-qwen3-8b")
    assert qwen.provider == "ollama"
    assert qwen.model == "qwen3:8b"
    assert {"filesystem", "python", "git"}.issubset({tool.id for tool in tools})
    assert mcps[0].transport == "stdio"

def test_registry_lookup():
    root = Path(__file__).parents[1]
    assert ModelRegistry(root / "models").get("ollama-qwen3-8b").name.startswith("Qwen3")
