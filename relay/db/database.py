import json
import uuid
from datetime import datetime, timezone

import aiosqlite

from relay.db.schema import ALL_TABLES, MessageRole, TaskStatus


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class DatabaseManager:
    """Async SQLite access layer for RELAY."""

    def __init__(self, db_path: str = "relay.db"):
        self.db_path = db_path
        self._conn: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        self._conn = await aiosqlite.connect(self.db_path)
        self._conn.row_factory = aiosqlite.Row
        await self._create_tables()

    async def disconnect(self) -> None:
        if self._conn:
            await self._conn.close()
            self._conn = None

    async def _create_tables(self) -> None:
        for ddl in ALL_TABLES:
            await self._conn.execute(ddl)
        await self._conn.commit()

    # ------------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------------

    async def create_task(self, description: str) -> dict:
        task = {
            "id": str(uuid.uuid4()),
            "description": description,
            "status": TaskStatus.PENDING.value,
            "created_at": _now(),
            "updated_at": _now(),
        }
        await self._conn.execute(
            "INSERT INTO tasks (id, description, status, created_at, updated_at) "
            "VALUES (:id, :description, :status, :created_at, :updated_at)",
            task,
        )
        await self._conn.commit()
        return task

    async def get_task(self, task_id: str) -> dict | None:
        async with self._conn.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def update_task_status(self, task_id: str, status: TaskStatus) -> None:
        await self._conn.execute(
            "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
            (status.value, _now(), task_id),
        )
        await self._conn.commit()

    # ------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------

    async def create_message(
        self, task_id: str, role: MessageRole, content: str
    ) -> dict:
        message = {
            "id": str(uuid.uuid4()),
            "task_id": task_id,
            "role": role.value,
            "content": content,
            "created_at": _now(),
        }
        await self._conn.execute(
            "INSERT INTO messages (id, task_id, role, content, created_at) "
            "VALUES (:id, :task_id, :role, :content, :created_at)",
            message,
        )
        await self._conn.commit()
        return message

    async def get_messages(self, task_id: str) -> list[dict]:
        async with self._conn.execute(
            "SELECT * FROM messages WHERE task_id = ? ORDER BY created_at",
            (task_id,),
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    # ------------------------------------------------------------------
    # Traces
    # ------------------------------------------------------------------

    async def create_trace(
        self, task_id: str, event: str, payload: dict | None = None
    ) -> dict:
        trace = {
            "id": str(uuid.uuid4()),
            "task_id": task_id,
            "event": event,
            "payload": json.dumps(payload) if payload else None,
            "created_at": _now(),
        }
        await self._conn.execute(
            "INSERT INTO traces (id, task_id, event, payload, created_at) "
            "VALUES (:id, :task_id, :event, :payload, :created_at)",
            trace,
        )
        await self._conn.commit()
        return trace

    async def get_traces(self, task_id: str) -> list[dict]:
        async with self._conn.execute(
            "SELECT * FROM traces WHERE task_id = ? ORDER BY created_at",
            (task_id,),
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]
