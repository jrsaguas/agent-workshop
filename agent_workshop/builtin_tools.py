from __future__ import annotations

from pathlib import Path
from typing import Any


class WorkspaceViolation(ValueError):
    """Raised when a filesystem operation escapes the configured workspace."""


def _resolve(workspace: Path, relative_path: str) -> Path:
    root = workspace.resolve()
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise WorkspaceViolation(f"path escapes workspace: {relative_path}") from exc
    return candidate


def filesystem_list(workspace: Path, path: str = ".") -> list[dict[str, Any]]:
    target = _resolve(workspace, path)
    if not target.is_dir():
        raise NotADirectoryError(path)
    return [{"name": p.name, "type": "directory" if p.is_dir() else "file"} for p in sorted(target.iterdir(), key=lambda x: x.name.lower())]


def filesystem_read(workspace: Path, path: str) -> str:
    return _resolve(workspace, path).read_text(encoding="utf-8")


def filesystem_write(workspace: Path, path: str, content: str) -> str:
    target = _resolve(workspace, path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target.relative_to(workspace.resolve()).as_posix()


def filesystem_delete(workspace: Path, path: str) -> str:
    target = _resolve(workspace, path)
    if target.is_dir():
        raise IsADirectoryError(path)
    target.unlink()
    return target.relative_to(workspace.resolve()).as_posix()


def filesystem_handlers(workspace: Path) -> dict[str, Any]:
    return {
        "filesystem.list": lambda path=".": filesystem_list(workspace, path),
        "filesystem.read": lambda path: filesystem_read(workspace, path),
        "filesystem.write": lambda path, content: filesystem_write(workspace, path, content),
        "filesystem.delete": lambda path: filesystem_delete(workspace, path),
    }
