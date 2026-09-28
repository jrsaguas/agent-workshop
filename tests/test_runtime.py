from pathlib import Path
from agent_workshop.runtime import AgentRuntime

def test_runtime_resolves_agent_resources():
    runtime = AgentRuntime(Path(__file__).parents[1])
    execution = runtime.prepare("python-engineer")
    assert execution.status == "running"
    assert execution.events[1].type == "agent.resolved"
    assert runtime.authorize(execution, "python-engineer", "filesystem.write") is False

def test_runtime_records_authorization():
    runtime = AgentRuntime(Path(__file__).parents[1])
    execution = runtime.prepare("python-engineer")
    assert runtime.authorize(execution, "python-engineer", "runtime.execute") is False
    assert execution.events[-1].data["allowed"] is False
