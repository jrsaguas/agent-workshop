from __future__ import annotations
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any
from .execution import Execution

class ExecutionStore:
    """Append/read execution records as JSON files."""
    def __init__(self, root: Path = Path("executions")) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, execution: Execution) -> Path:
        path = self.root / f"{execution.execution_id}.json"
        payload = asdict(execution)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def load(self, execution_id: str) -> dict[str, Any]:
        path = self.root / f"{execution_id}.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def list(self) -> list[str]:
        return sorted(p.stem for p in self.root.glob("*.json"))
