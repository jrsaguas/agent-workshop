from pathlib import Path
from agent_workshop.registry import AgentRegistry
def test_load_example():
    agent = AgentRegistry(Path("examples")).load(Path("examples/python-engineer.agent.yaml"))
    assert agent.id == "python-engineer"
    assert agent.model["provider"] == "ollama"
    assert agent.capabilities["coding"] is True
