from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Generic, TypeVar, Callable
import yaml

T = TypeVar("T")

@dataclass
class ResourceRegistry(Generic[T]):
    root: Path
    factory: Callable[[dict[str, Any]], T]
    suffix: str
    _items: dict[str, T] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)

    def load(self, path: Path) -> T:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        resource = data.get(self.suffix)
        if not isinstance(resource, dict):
            raise ValueError(f"{path}: expected root key '{self.suffix}'")
        item = self.factory(resource)
        identifier = resource.get("id")
        if not isinstance(identifier, str) or not identifier:
            raise ValueError(f"{path}: resource requires a non-empty id")
        self._items[identifier] = item
        return item

    def list(self) -> list[T]:
        for path in sorted(self.root.glob(f"*.{self.suffix}.yaml")):
            self.load(path)
        return list(self._items.values())

    def get(self, identifier: str) -> T | None:
        if not self._items:
            self.list()
        return self._items.get(identifier)
