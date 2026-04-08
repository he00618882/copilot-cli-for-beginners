from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_DATA: dict[str, Any] = {"tasks": [], "next_id": 1}


class StorageError(Exception):
    """Raised when task storage cannot be read or written."""


def load_data(file_path: Path) -> dict[str, Any]:
    """Load task data from a JSON file or return defaults if it does not exist."""
    if not file_path.exists():
        return {"tasks": [], "next_id": 1}

    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise StorageError(f"無法解析 JSON 檔案：{file_path}") from exc
    except OSError as exc:
        raise StorageError(f"無法讀取檔案：{file_path}") from exc

    if not isinstance(data, dict) or "tasks" not in data or "next_id" not in data:
        raise StorageError(f"資料格式錯誤：{file_path}")

    tasks = data.get("tasks")
    next_id = data.get("next_id")

    if not isinstance(tasks, list) or not isinstance(next_id, int):
        raise StorageError(f"資料欄位型別錯誤：{file_path}")

    return data


def save_data(file_path: Path, data: dict[str, Any]) -> None:
    """Persist task data to JSON."""
    try:
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as exc:
        raise StorageError(f"無法寫入檔案：{file_path}") from exc
