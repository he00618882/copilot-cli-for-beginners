from __future__ import annotations

import json
from pathlib import Path

import pytest

from todo_cli.__main__ import main, render_tasks
from todo_cli.app import TaskNotFoundError, TodoApp, ValidationError
from todo_cli.storage import StorageError, load_data


@pytest.fixture
def task_file(tmp_path: Path) -> Path:
    return tmp_path / "tasks.json"


class TestTodoApp:
    def test_add_and_list_tasks(self, task_file: Path) -> None:
        app = TodoApp(task_file)

        first = app.add_task("買牛奶")
        second = app.add_task("寫報告")

        assert first["id"] == 1
        assert second["id"] == 2
        assert [t["title"] for t in app.list_tasks()] == ["買牛奶", "寫報告"]

    def test_add_empty_title_raises_validation_error(self, task_file: Path) -> None:
        app = TodoApp(task_file)

        with pytest.raises(ValidationError):
            app.add_task("   ")

    def test_complete_task(self, task_file: Path) -> None:
        app = TodoApp(task_file)
        app.add_task("測試完成")

        completed = app.complete_task(1)

        assert completed["completed"] is True
        assert app.list_tasks()[0]["completed"] is True

    def test_complete_missing_task_raises(self, task_file: Path) -> None:
        app = TodoApp(task_file)

        with pytest.raises(TaskNotFoundError):
            app.complete_task(999)

    def test_delete_task(self, task_file: Path) -> None:
        app = TodoApp(task_file)
        app.add_task("要刪除")

        app.delete_task(1)

        assert app.list_tasks() == []

    def test_delete_missing_task_raises(self, task_file: Path) -> None:
        app = TodoApp(task_file)

        with pytest.raises(TaskNotFoundError):
            app.delete_task(404)


class TestCli:
    def test_main_add_list_complete_delete_flow(self, task_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
        assert main(["--file", str(task_file), "add", "任務 A"]) == 0
        out = capsys.readouterr().out
        assert "已新增任務 #1" in out

        assert main(["--file", str(task_file), "list"]) == 0
        out = capsys.readouterr().out
        assert "[ ] 1: 任務 A" in out

        assert main(["--file", str(task_file), "complete", "1"]) == 0
        out = capsys.readouterr().out
        assert "已完成任務 #1" in out

        assert main(["--file", str(task_file), "delete", "1"]) == 0
        out = capsys.readouterr().out
        assert "已刪除任務 #1" in out

    def test_main_returns_error_for_missing_task(self, task_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
        result = main(["--file", str(task_file), "delete", "2"])
        err = capsys.readouterr().err

        assert result == 1
        assert "錯誤：找不到 ID=2 的任務" in err

    def test_render_tasks_empty(self) -> None:
        assert render_tasks([]) == "目前沒有任務"


def test_load_data_invalid_json_raises(tmp_path: Path) -> None:
    file_path = tmp_path / "broken.json"
    file_path.write_text("{bad json", encoding="utf-8")

    with pytest.raises(StorageError):
        load_data(file_path)


def test_json_file_structure_after_add(task_file: Path) -> None:
    app = TodoApp(task_file)
    app.add_task("檢查結構")

    raw = json.loads(task_file.read_text(encoding="utf-8"))

    assert set(raw.keys()) == {"tasks", "next_id"}
    assert raw["next_id"] == 2
    assert raw["tasks"][0]["title"] == "檢查結構"
