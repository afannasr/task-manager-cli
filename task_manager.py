"""Task Manager CLI - a small command-line to-do app.

Skills shown: Python OOP, lists/dicts, JSON file storage, functions,
argparse (command-line arguments), error handling.
"""
import argparse
import json
import os
from datetime import datetime

DATA_FILE = "tasks.json"


class Task:
    """One to-do item."""

    def __init__(self, task_id, title, done=False, created=None):
        self.task_id = task_id
        self.title = title
        self.done = done
        self.created = created or datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "done": self.done,
            "created": self.created,
        }

    @staticmethod
    def from_dict(data):
        return Task(data["id"], data["title"], data["done"], data["created"])

    def __str__(self):
        mark = "[x]" if self.done else "[ ]"
        return f"{self.task_id:>3}. {mark} {self.title}  ({self.created})"


class TaskManager:
    """Keeps all tasks and saves them to a JSON file."""

    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.tasks = []
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.tasks = [Task.from_dict(d) for d in json.load(f)]
        except (json.JSONDecodeError, KeyError):
            print("Warning: tasks file is damaged. Starting with an empty list.")
            self.tasks = []

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=2)

    def _next_id(self):
        return max((t.task_id for t in self.tasks), default=0) + 1

    def add(self, title):
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        task = Task(self._next_id(), title)
        self.tasks.append(task)
        self.save()
        return task

    def find(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        raise KeyError(f"No task with id {task_id}.")

    def complete(self, task_id):
        task = self.find(task_id)
        task.done = True
        self.save()
        return task

    def delete(self, task_id):
        task = self.find(task_id)
        self.tasks.remove(task)
        self.save()
        return task

    def list_tasks(self, show_done=True):
        if show_done:
            return list(self.tasks)
        return [t for t in self.tasks if not t.done]


def build_parser():
    parser = argparse.ArgumentParser(description="Simple Task Manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task title (use quotes)")

    p_list = sub.add_parser("list", help="Show tasks")
    p_list.add_argument("--pending", action="store_true", help="Only unfinished tasks")

    p_done = sub.add_parser("done", help="Mark a task as done")
    p_done.add_argument("task_id", type=int)

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("task_id", type=int)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    manager = TaskManager()
    try:
        if args.command == "add":
            task = manager.add(args.title)
            print(f"Added: {task}")
        elif args.command == "list":
            tasks = manager.list_tasks(show_done=not args.pending)
            if not tasks:
                print("No tasks found.")
            for task in tasks:
                print(task)
        elif args.command == "done":
            print(f"Completed: {manager.complete(args.task_id)}")
        elif args.command == "delete":
            print(f"Deleted: {manager.delete(args.task_id)}")
    except (ValueError, KeyError) as error:
        print(f"Error: {error.args[0]}")


if __name__ == "__main__":
    main()
                 
