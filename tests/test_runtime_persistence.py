from pathlib import Path

import pytest

from agent_workshop.execution_store import ExecutionStore
from agent_workshop.providers import ProviderRegistry
from agent_workshop.runtime import AgentRuntime


class FakeProvider:
    def __init__(self, response="ok", error=None):
        self.response = response
        self.error = error

    def generate(self, model, prompt, **options):
        if self.error:
            raise RuntimeError(self.error)
        return self.response


def test_runtime_persists_completed_execution(tmp_path: Path):
    provider = FakeProvider(response="2+2=4")
    runtime = AgentRuntime(tmp_path, providers=ProviderRegistry({"ollama": provider}), execution_store=ExecutionStore(tmp_path / "executions"))
    agent_dir = tmp_path / "agents"
    model_dir = tmp_path / "models"
    tool_dir = tmp_path / "tools"
    mcp_dir = tmp_path / "mcp"
    for directory in (agent_dir, model_dir, tool_dir, mcp_dir):
        directory.mkdir()
    (agent_dir / "demo.agent.yaml").write_text("""agent:\n  id: demo\n  name: Demo\n  version: 1.0.0\n  model:\n    id: demo-model\n  instructions: test\n  tools: []\n  mcp: []\n  permissions:\n    default: deny\n""", encoding="utf-8")
    (model_dir / "demo.model.yaml").write_text("""model:\n  id: demo-model\n  name: Demo\n  provider: ollama\n  model: fake\n""", encoding="utf-8")
    execution, response = runtime.generate("demo", "hello")
    assert response == "2+2=4"
    saved = runtime.execution_store.load(execution.execution_id)
    assert saved["status"] == "completed"
    assert [event["type"] for event in saved["events"]][-1] == "execution.completed"


def test_runtime_persists_failed_execution(tmp_path: Path):
    provider = FakeProvider(error="provider failed")
    runtime = AgentRuntime(tmp_path, providers=ProviderRegistry({"ollama": provider}), execution_store=ExecutionStore(tmp_path / "executions"))
    for directory in (tmp_path / "agents", tmp_path / "models", tmp_path / "tools", tmp_path / "mcp"):
        directory.mkdir()
    (tmp_path / "agents" / "demo.agent.yaml").write_text("""agent:\n  id: demo\n  name: Demo\n  version: 1.0.0\n  model:\n    id: demo-model\n  instructions: test\n  tools: []\n  mcp: []\n  permissions:\n    default: deny\n""", encoding="utf-8")
    (tmp_path / "models" / "demo.model.yaml").write_text("""model:\n  id: demo-model\n  name: Demo\n  provider: ollama\n  model: fake\n""", encoding="utf-8")
    with pytest.raises(RuntimeError, match="provider failed"):
        runtime.generate("demo", "hello")
    executions = runtime.execution_store.list()
    assert len(executions) == 1
    saved = runtime.execution_store.load(executions[0])
    assert saved["status"] == "failed"
    assert saved["events"][-1]["type"] == "execution.failed"
