"""
RELAY Engine — Phase 2

The engine is the central coordinator for RELAY. Think of it like the
expeditor at a restaurant: every order (task) comes through here, gets
logged, and is passed to the right station (agent).

Phase 2 scope: task intake + persistence. Agent routing comes in Phase 4/5.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone

from relay.db.database import DatabaseManager
from relay.db.schema import MessageRole, TaskStatus


@dataclass
class RelayMessage:
    """A single message passed between agents through the RELAY engine."""

    task_id: str
    role: MessageRole
    content: str
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "role": self.role.value,
            "content": self.content,
            "created_at": self.created_at,
        }


class RelayEngine:
    """
    Central coordinator for RELAY.

    Responsibilities:
    - Accept tasks from users or the API layer
    - Persist tasks, messages, and trace events to SQLite
    - (Future phases) Route messages between Seraph and Daedalus
    """

    def __init__(self, db_path: str = "relay.db"):
        self.db = DatabaseManager(db_path)
        self._running = False

    async def start(self) -> None:
        """Connect to the database and mark the engine as ready."""
        await self.db.connect()
        self._running = True
        print("[RELAY] Engine started.")

    async def stop(self) -> None:
        """Gracefully shut down the engine."""
        await self.db.disconnect()
        self._running = False
        print("[RELAY] Engine stopped.")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def submit_task(self, description: str) -> dict:
        """
        Accept a new task, persist it, and return the task record.

        This is the main entry point — the equivalent of a customer
        placing an order at the counter.
        """
        task = await self.db.create_task(description)

        await self.db.create_trace(
            task_id=task["id"],
            event="task_submitted",
            payload={"description": description},
        )

        print(f"[RELAY] Task submitted: {task['id']}")
        print(f"        '{description}'")
        return task

    async def send_message(
        self, task_id: str, role: MessageRole, content: str
    ) -> RelayMessage:
        """
        Log a message on a task and return a RelayMessage object.

        In Phase 4/5 this will also dispatch the message to the
        appropriate agent. For now it just persists it.
        """
        await self.db.create_message(task_id, role, content)
        await self.db.create_trace(
            task_id=task_id,
            event="message_logged",
            payload={"role": role.value, "preview": content[:80]},
        )

        msg = RelayMessage(task_id=task_id, role=role, content=content)
        print(f"[RELAY] Message [{role.value}] → task {task_id[:8]}…")
        return msg

    async def complete_task(self, task_id: str) -> None:
        """Mark a task as completed."""
        await self.db.update_task_status(task_id, TaskStatus.COMPLETED)
        await self.db.create_trace(task_id=task_id, event="task_completed")
        print(f"[RELAY] Task {task_id[:8]}… completed.")

    async def fail_task(self, task_id: str, reason: str) -> None:
        """Mark a task as failed and record the reason."""
        await self.db.update_task_status(task_id, TaskStatus.FAILED)
        await self.db.create_trace(
            task_id=task_id,
            event="task_failed",
            payload={"reason": reason},
        )
        print(f"[RELAY] Task {task_id[:8]}… FAILED: {reason}")

    # ------------------------------------------------------------------
    # Inspection helpers
    # ------------------------------------------------------------------

    async def get_task(self, task_id: str) -> dict | None:
        return await self.db.get_task(task_id)

    async def get_messages(self, task_id: str) -> list[dict]:
        return await self.db.get_messages(task_id)

    async def get_traces(self, task_id: str) -> list[dict]:
        return await self.db.get_traces(task_id)
