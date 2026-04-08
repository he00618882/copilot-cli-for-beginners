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


class TestAcceptanceCriteria:
    """PRD 驗收準則：新增、列出、標記完成、刪除與持久化。"""

    def test_add_persists_to_json(self, task_file: Path) -> None:
        app = TodoApp(task_file)

        created = app.add_task("買牛奶")
        raw = json.loads(task_file.read_text(encoding="utf-8"))

        assert created["id"] == 1
        assert raw["tasks"][0]["title"] == "買牛奶"
        assert raw["tasks"][0]["completed"] is False
        assert raw["next_id"] == 2

    def test_list_displays_task_status(self, task_file: Path) -> None:
        app = TodoApp(task_file)
        app.add_task("任務 A")
        app.add_task("任務 B")
        app.complete_task(2)

        rendered = render_tasks(app.list_tasks())

        assert "[ ] 1: 任務 A" in rendered
        assert "[x] 2: 任務 B" in rendered

    def test_complete_updates_target_task(self, task_file: Path) -> None:
        app = TodoApp(task_file)
        app.add_task("完成我")

        app.complete_task(1)

        tasks = app.list_tasks()
        assert tasks[0]["completed"] is True

    def test_delete_removes_target_task(self, task_file: Path) -> None:
        app = TodoApp(task_file)
        app.add_task("刪我")

        app.delete_task(1)

        assert app.list_tasks() == []

    def test_data_remains_after_restart(self, task_file: Path) -> None:
        first = TodoApp(task_file)
        first.add_task("重啟後仍存在")

        second = TodoApp(task_file)
        tasks = second.list_tasks()

        assert len(tasks) == 1
        assert tasks[0]["title"] == "重啟後仍存在"


class TestEdgeCases:
    @pytest.mark.parametrize("title", ["", "   ", "\n\t"])
    def test_add_rejects_empty_title(self, task_file: Path, title: str) -> None:
        app = TodoApp(task_file)

        with pytest.raises(ValidationError):
            app.add_task(title)

    @pytest.mark.parametrize("missing_id", [0, 999])
    def test_complete_missing_id_raises(self, task_file: Path, missing_id: int) -> None:
        app = TodoApp(task_file)

        with pytest.raises(TaskNotFoundError):
            app.complete_task(missing_id)

    @pytest.mark.parametrize("missing_id", [0, 999])
    def test_delete_missing_id_raises(self, task_file: Path, missing_id: int) -> None:
        app = TodoApp(task_file)

        with pytest.raises(TaskNotFoundError):
            app.delete_task(missing_id)

    def test_load_data_returns_default_for_nonexistent_file(self, tmp_path: Path) -> None:
        missing_file = tmp_path / "missing.json"

        data = load_data(missing_file)

        assert data == {"tasks": [], "next_id": 1}

    def test_load_data_raises_on_invalid_json(self, tmp_path: Path) -> None:
        broken_file = tmp_path / "broken.json"
        broken_file.write_text("{invalid", encoding="utf-8")

        with pytest.raises(StorageError):
            load_data(broken_file)


class TestCliIntegration:
    def test_cli_main_flow(self, task_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
        assert main(["--file", str(task_file), "add", "任務 A"]) == 0
        assert "已新增任務 #1" in capsys.readouterr().out

        assert main(["--file", str(task_file), "list"]) == 0
        assert "[ ] 1: 任務 A" in capsys.readouterr().out

        assert main(["--file", str(task_file), "complete", "1"]) == 0
        assert "已完成任務 #1" in capsys.readouterr().out

        assert main(["--file", str(task_file), "delete", "1"]) == 0
        assert "已刪除任務 #1" in capsys.readouterr().out

    def test_cli_returns_error_for_unknown_task(self, task_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
        result = main(["--file", str(task_file), "complete", "123"])
        captured = capsys.readouterr()

        assert result == 1
        assert "錯誤：找不到 ID=123 的任務" in captured.err

    def test_render_tasks_when_empty(self) -> None:
        assert render_tasks([]) == "目前沒有任務"