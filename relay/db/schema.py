from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class MessageRole(str, Enum):
    USER = "user"
    SERAPH = "seraph"
    DAEDALUS = "daedalus"
    RELAY = "relay"


class AgentName(str, Enum):
    SERAPH = "seraph"
    DAEDALUS = "daedalus"


# SQL DDL — all three tables RELAY needs

CREATE_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id          TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'pending',
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);
"""

CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    id          TEXT PRIMARY KEY,
    task_id     TEXT NOT NULL,
    role        TEXT NOT NULL,
    content     TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);
"""

CREATE_TRACES_TABLE = """
CREATE TABLE IF NOT EXISTS traces (
    id          TEXT PRIMARY KEY,
    task_id     TEXT NOT NULL,
    event       TEXT NOT NULL,
    payload     TEXT,
    created_at  TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);
"""

ALL_TABLES = [CREATE_TASKS_TABLE, CREATE_MESSAGES_TABLE, CREATE_TRACES_TABLE]
