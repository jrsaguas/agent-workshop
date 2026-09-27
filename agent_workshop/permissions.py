from __future__ import annotations
from dataclasses import dataclass
from fnmatch import fnmatch
from typing import Any

@dataclass(frozen=True)
class PermissionRule:
    operation: str
    effect: str
    resource: str = "*"

class PermissionPolicy:
    """Deterministic permission evaluator; deny-by-default is the safe default."""
    def __init__(self, data: dict[str, Any] | None = None):
        data = data or {}
        self.default = data.get("default", "deny")
        self.rules = tuple(PermissionRule(r["operation"], r["effect"], r.get("resource", "*")) for r in data.get("rules", []))
        if self.default not in {"deny", "allow"}:
            raise ValueError("default must be 'deny' or 'allow'")

    def allows(self, operation: str, resource: str = "*") -> bool:
        for rule in self.rules:
            if fnmatch(operation, rule.operation) and fnmatch(resource, rule.resource):
                return rule.effect == "allow"
        return self.default == "allow"
