from agent_workshop.permissions import PermissionPolicy
from agent_workshop.resource_models import ToolDefinition
from agent_workshop.execution import Execution
from agent_workshop.tool_executor import ToolExecutor

def test_tool_executor_denies_by_default():
    tool = ToolDefinition("python", "Python", "builtin", permission="runtime.execute")
    execution = Execution("test")
    result = ToolExecutor({"python": lambda **_: 42}).execute(tool, execution, PermissionPolicy())
    assert result.success is False
    assert result.error == "permission denied"

def test_tool_executor_runs_authorized_handler():
    tool = ToolDefinition("python", "Python", "builtin", permission="runtime.execute")
    execution = Execution("test")
    policy = PermissionPolicy({"default": "deny", "rules": [{"operation": "runtime.execute", "resource": "*", "effect": "allow"}]})
    result = ToolExecutor({"python": lambda **_: 42}).execute(tool, execution, policy)
    assert result.success is True
    assert result.output == 42
    assert execution.events[-1].type == "tool.completed"
