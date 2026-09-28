from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any

@dataclass(frozen=True)
class ExecutionEvent:
    type: str
    timestamp: str
    data: dict[str, Any] = field(default_factory=dict)

@dataclass
class Execution:
    agent_id: str
    execution_id: str = field(default_factory=lambda: str(uuid4()))
    status: str = "created"
    events: list[ExecutionEvent] = field(default_factory=list)

    def record(self, event_type: str, **data: Any) -> None:
        self.events.append(ExecutionEvent(event_type, datetime.now(timezone.utc).isoformat(), data))

    def start(self) -> None:
        self.status = "running"
        self.record("execution.started", agent_id=self.agent_id)

    def complete(self) -> None:
        self.status = "completed"
        self.record("execution.completed")

    def fail(self, error: str) -> None:
        self.status = "failed"
        self.record("execution.failed", error=error)
