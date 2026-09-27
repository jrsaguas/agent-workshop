from dataclasses import dataclass, field
from typing import Any
@dataclass
class AgentDefinition:
    id: str
    name: str
    version: str
    model: dict[str, Any]
    instructions: str
    description: str = ""
    capabilities: dict[str, bool] = field(default_factory=dict)
    tools: list[str] = field(default_factory=list)
    mcp: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    memory: dict[str, Any] = field(default_factory=dict)
    permissions: dict[str, Any] = field(default_factory=dict)
    runtime: dict[str, Any] = field(default_factory=dict)
    subagents: list[str] = field(default_factory=list)
    evaluation: dict[str, Any] = field(default_factory=dict)
