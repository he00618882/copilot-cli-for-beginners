from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .app import TaskNotFoundError, TodoApp, ValidationError
from .storage import StorageError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="命令列 To-Do List 應用程式")
    parser.add_argument("--file", default="tasks.json", help="JSON 儲存檔案路徑")

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="新增任務")
    add_parser.add_argument("title", help="任務標題")

    subparsers.add_parser("list", help="列出任務")

    complete_parser = subparsers.add_parser("complete", help="標記完成")
    complete_parser.add_argument("id", type=int, help="任務 ID")

    delete_parser = subparsers.add_parser("delete", help="刪除任務")
    delete_parser.add_argument("id", type=int, help="任務 ID")

    return parser


def render_tasks(tasks: list[dict[str, object]]) -> str:
    if not tasks:
        return "目前沒有任務"

    lines: list[str] = []
    for task in tasks:
        marker = "x" if task["completed"] else " "
        lines.append(f"[{marker}] {task['id']}: {task['title']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    app = TodoApp(file_path=Path(args.file))

    try:
        if args.command == "add":
            task = app.add_task(args.title)
            print(f"已新增任務 #{task['id']}: {task['title']}")
            return 0

        if args.command == "list":
            print(render_tasks(app.list_tasks()))
            return 0

        if args.command == "complete":
            task = app.complete_task(args.id)
            print(f"已完成任務 #{task['id']}: {task['title']}")
            return 0

        if args.command == "delete":
            app.delete_task(args.id)
            print(f"已刪除任務 #{args.id}")
            return 0

        parser.print_help()
        return 1

    except (ValidationError, TaskNotFoundError, StorageError) as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
