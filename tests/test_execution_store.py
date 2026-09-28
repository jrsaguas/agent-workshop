from agent_workshop.execution import Execution
from agent_workshop.execution_store import ExecutionStore


def test_execution_store_roundtrip(tmp_path):
    store = ExecutionStore(tmp_path / "executions")
    execution = Execution("python-engineer")
    execution.start()
    execution.record("test.event", value=42)
    execution.complete()
    path = store.save(execution)
    assert path.exists()
    data = store.load(execution.execution_id)
    assert data["agent_id"] == "python-engineer"
    assert data["status"] == "completed"
    assert data["events"][-1]["type"] == "execution.completed"
    assert store.list() == [execution.execution_id]
