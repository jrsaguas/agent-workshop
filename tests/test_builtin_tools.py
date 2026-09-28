from pathlib import Path

import pytest

from agent_workshop.builtin_tools import WorkspaceViolation, filesystem_delete, filesystem_list, filesystem_read, filesystem_write


def test_filesystem_read_write_list_and_delete(tmp_path: Path):
    filesystem_write(tmp_path, "src/example.py", "print('ok')\n")
    assert filesystem_read(tmp_path, "src/example.py") == "print('ok')\n"
    entries = filesystem_list(tmp_path, "src")
    assert entries == [{"name": "example.py", "type": "file"}]
    assert filesystem_delete(tmp_path, "src/example.py") == "src/example.py"
    assert not (tmp_path / "src/example.py").exists()


def test_filesystem_blocks_path_traversal(tmp_path: Path):
    outside = tmp_path.parent / "outside.txt"
    outside.write_text("secret", encoding="utf-8")
    with pytest.raises(WorkspaceViolation):
        filesystem_read(tmp_path, "../outside.txt")


def test_filesystem_blocks_absolute_escape(tmp_path: Path):
    with pytest.raises(WorkspaceViolation):
        filesystem_write(tmp_path, str(tmp_path.parent / "escape.txt"), "blocked")


def test_filesystem_delete_cannot_delete_directory(tmp_path: Path):
    (tmp_path / "folder").mkdir()
    with pytest.raises(IsADirectoryError):
        filesystem_delete(tmp_path, "folder")
