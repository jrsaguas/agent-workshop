from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ModelDefinition:
    id: str
    name: str
    provider: str
    model: str
    kind: str = "chat"
    capabilities: tuple[str, ...] = ()
    context_window: int | None = None
    config: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class ToolDefinition:
    id: str
    name: str
    kind: str
    description: str = ""
    capabilities: tuple[str, ...] = ()
    input_schema: dict[str, Any] = field(default_factory=dict)
    permission: str | None = None

@dataclass(frozen=True)
class MCPServerDefinition:
    id: str
    name: str
    transport: str
    command: str | None = None
    args: tuple[str, ...] = ()
    url: str | None = None
    env: dict[str, str] = field(default_factory=dict)
    tools: tuple[str, ...] = ()
