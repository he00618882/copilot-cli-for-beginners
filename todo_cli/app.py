from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .storage import load_data, save_data


class TaskNotFoundError(Exception):
    """Raised when task id cannot be found."""


class ValidationError(Exception):
    """Raised when user input is invalid."""


@dataclass
class TodoApp:
    file_path: Path

    def add_task(self, title: str) -> dict[str, Any]:
        normalized_title = title.strip()
        if not normalized_title:
            raise ValidationError("任務標題不可為空")

        data = load_data(self.file_path)
        task = {
            "id": data["next_id"],
            "title": normalized_title,
            "completed": False,
        }
        data["tasks"].append(task)
        data["next_id"] += 1
        save_data(self.file_path, data)
        return task

    def list_tasks(self) -> list[dict[str, Any]]:
        data = load_data(self.file_path)
        return data["tasks"]

    def complete_task(self, task_id: int) -> dict[str, Any]:
        data = load_data(self.file_path)
        for task in data["tasks"]:
            if task["id"] == task_id:
                task["completed"] = True
                save_data(self.file_path, data)
                return task
        raise TaskNotFoundError(f"找不到 ID={task_id} 的任務")

    def delete_task(self, task_id: int) -> None:
        data = load_data(self.file_path)
        original_length = len(data["tasks"])
        data["tasks"] = [task for task in data["tasks"] if task["id"] != task_id]
        if len(data["tasks"]) == original_length:
            raise TaskNotFoundError(f"找不到 ID={task_id} 的任務")
        save_data(self.file_path, data)
