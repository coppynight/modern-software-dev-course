"""每次操作使用独立连接，适配教学 HTTP 服务的请求线程。"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from app.domain import clean_title


class Store:
    def __init__(self, path):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0 CHECK(done IN (0, 1))
            )""")

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    @staticmethod
    def as_task(row):
        return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}

    def list(self):
        with self.connection() as db:
            return [self.as_task(r) for r in db.execute("SELECT * FROM tasks ORDER BY id")]

    def add(self, title):
        title = clean_title(title)
        with self.connection() as db:
            cursor = db.execute("INSERT INTO tasks(title) VALUES (?)", (title,))
            return self.as_task(db.execute("SELECT * FROM tasks WHERE id=?", (cursor.lastrowid,)).fetchone())

    def update(self, task_id, changes):
        if not isinstance(changes, dict) or not changes or set(changes) - {"title", "done"}:
            raise ValueError("只接受 title 或 done，且至少提供一项")
        if "done" in changes and type(changes["done"]) is not bool:
            raise ValueError("done 必须是布尔值")
        title = clean_title(changes["title"]) if "title" in changes else None
        with self.connection() as db:
            row = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
            if row is None:
                raise KeyError(task_id)
            db.execute("UPDATE tasks SET title=?, done=? WHERE id=?", (
                title if title is not None else row["title"],
                int(changes.get("done", bool(row["done"]))), task_id))
            return self.as_task(db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone())

    def delete(self, task_id):
        with self.connection() as db:
            if db.execute("DELETE FROM tasks WHERE id=?", (task_id,)).rowcount == 0:
                raise KeyError(task_id)
