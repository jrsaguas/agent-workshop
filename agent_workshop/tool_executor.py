from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .execution import Execution
from .permissions import PermissionPolicy
from .resource_models import ToolDefinition


class ToolInputError(ValueError):
    pass


@dataclass
class ToolResult:
    tool_id: str
    success: bool
    output: Any = None
    error: str | None = None


class ToolExecutor:
    def __init__(self, handlers: dict[str, Callable[..., Any]] | None = None):
        self.handlers = handlers or {}

    def execute(self, tool: ToolDefinition, execution: Execution, policy: PermissionPolicy, **arguments: Any) -> ToolResult:
        required = tool.input_schema.get("required", [])
        missing = [name for name in required if name not in arguments]
        if missing:
            error = f"missing required arguments: {', '.join(missing)}"
            execution.record("tool.invalid_input", tool=tool.id, error=error)
            return ToolResult(tool.id, False, error=error)
        properties = tool.input_schema.get("properties", {})
        if tool.input_schema.get("additionalProperties") is False:
            unknown = sorted(set(arguments) - set(properties))
            if unknown:
                error = f"unknown arguments: {', '.join(unknown)}"
                execution.record("tool.invalid_input", tool=tool.id, error=error)
                return ToolResult(tool.id, False, error=error)
        resource = str(arguments.get("resource", "*"))
        operation = tool.permission or f"tool.{tool.id}"
        allowed = policy.allows(operation, resource)
        execution.record("tool.authorization", tool=tool.id, operation=operation, resource=resource, allowed=allowed)
        if not allowed:
            return ToolResult(tool.id, False, error="permission denied")
        handler = self.handlers.get(tool.id)
        if handler is None:
            execution.record("tool.unavailable", tool=tool.id)
            return ToolResult(tool.id, False, error="tool handler not configured")
        try:
            output = handler(**arguments)
            execution.record("tool.completed", tool=tool.id)
            return ToolResult(tool.id, True, output=output)
        except Exception as exc:
            execution.record("tool.failed", tool=tool.id, error=str(exc))
            return ToolResult(tool.id, False, error=str(exc))
