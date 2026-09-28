from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

from .builtin_tools import WorkspaceViolation, _resolve


def python_run(workspace: Path, path: str, timeout: float = 10.0, args: list[str] | None = None) -> dict[str, Any]:
    """Run a Python file inside the workspace. This is not an OS-level sandbox."""
    if timeout <= 0 or timeout > 120:
        raise ValueError("timeout must be > 0 and <= 120 seconds")
    script = _resolve(workspace, path)
    if not script.is_file() or script.suffix.lower() != ".py":
        raise ValueError("path must identify an existing .py file")
    try:
        completed = subprocess.run(
            [sys.executable, "-I", str(script), *(args or [])],
            cwd=str(workspace.resolve()), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout, check=False,
        )
        return {"returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr, "timed_out": False}
    except subprocess.TimeoutExpired as exc:
        return {
            "returncode": None,
            "stdout": (exc.stdout or b"").decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or ""),
            "stderr": (exc.stderr or b"").decode("utf-8", "replace") if isinstance(exc.stderr, bytes) else (exc.stderr or ""),
            "timed_out": True,
        }


_GIT_READ_COMMANDS = {
    "status": ["status", "--short", "--branch"],
    "diff": ["diff", "--no-ext-diff", "--"],
    "log": ["log", "-10", "--oneline", "--decorate"],
    "branches": ["branch", "--list"],
}


def git_read(workspace: Path, operation: str, timeout: float = 10.0) -> dict[str, Any]:
    if operation not in _GIT_READ_COMMANDS:
        raise ValueError(f"unsupported read-only Git operation: {operation}")
    if timeout <= 0 or timeout > 30:
        raise ValueError("timeout must be > 0 and <= 30 seconds")
    root = workspace.resolve()
    if not (root / ".git").exists():
        raise ValueError("workspace is not a Git repository")
    completed = subprocess.run(
        ["git", *_GIT_READ_COMMANDS[operation]], cwd=str(root),
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=timeout, check=False,
    )
    return {"returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}


def process_tool_handlers(workspace: Path) -> dict[str, Any]:
    return {
        "python": lambda path, timeout=10.0, args=None: python_run(workspace, path, timeout, args),
        "git": lambda operation, timeout=10.0: git_read(workspace, operation, timeout),
    }
