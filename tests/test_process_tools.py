from pathlib import Path

import pytest

from agent_workshop.process_tools import git_read, python_run


def test_python_run_success(tmp_path: Path):
    script = tmp_path / "hello.py"
    script.write_text("print('hello')", encoding="utf-8")
    result = python_run(tmp_path, "hello.py")
    assert result["returncode"] == 0
    assert result["stdout"].strip() == "hello"
    assert result["timed_out"] is False


def test_python_run_failure_captures_stderr(tmp_path: Path):
    script = tmp_path / "bad.py"
    script.write_text("raise RuntimeError('boom')", encoding="utf-8")
    result = python_run(tmp_path, "bad.py")
    assert result["returncode"] != 0
    assert "boom" in result["stderr"]


def test_python_run_timeout(tmp_path: Path):
    script = tmp_path / "slow.py"
    script.write_text("import time; time.sleep(2)", encoding="utf-8")
    result = python_run(tmp_path, "slow.py", timeout=0.1)
    assert result["timed_out"] is True
    assert result["returncode"] is None


def test_python_run_blocks_non_python_and_escape(tmp_path: Path):
    (tmp_path / "note.txt").write_text("x", encoding="utf-8")
    with pytest.raises(ValueError):
        python_run(tmp_path, "note.txt")
    with pytest.raises(ValueError):
        python_run(tmp_path, "../outside.py")


def test_git_read_only_operations(tmp_path: Path):
    import subprocess
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    result = git_read(tmp_path, "status")
    assert result["returncode"] == 0
    assert "##" in result["stdout"]


def test_git_read_rejects_write_operations(tmp_path: Path):
    import subprocess
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    with pytest.raises(ValueError):
        git_read(tmp_path, "commit")
