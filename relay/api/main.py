# relay/api/main.py
import os
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from relay.agents.seraph import SeraphAgent
from relay.agents.daedalus import DaedalusAgent
from relay.coordinator import RelayCoordinator

load_dotenv()

app = FastAPI(
    title="RELAY Multi-Agent Platform",
    description="API for coordinating Seraph and Daedalus agents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

seraph = SeraphAgent()
daedalus = DaedalusAgent()
coordinator = RelayCoordinator()

tasks = {}


class TaskRequest(BaseModel):
    description: str


class SubtaskRequest(BaseModel):
    subtask: str


class PipelineRequest(BaseModel):
    description: str


@app.get("/")
def root():
    return {
        "system": "RELAY Multi-Agent Platform",
        "version": "1.0.0",
        "status": "online",
        "agents": ["seraph", "daedalus"]
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/tasks")
def create_task(request: TaskRequest):
    task_id = str(uuid.uuid4())
    plan = seraph.create_plan(request.description)
    tasks[task_id] = {
        "id": task_id,
        "description": request.description,
        "status": "planned",
        "plan": plan
    }
    return {
        "task_id": task_id,
        "status": "planned",
        "plan": plan
    }


@app.get("/tasks")
def list_tasks():
    return {"tasks": list(tasks.values())}


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.post("/execute")
def execute_subtask(request: SubtaskRequest):
    result = daedalus.execute(request.subtask)
    return {
        "subtask": request.subtask,
        "result": result
    }


@app.get("/agents")
def list_agents():
    return {
        "agents": [
            {
                "name": seraph.identity.name,
                "role": seraph.identity.role,
                "version": seraph.identity.version,
                "capabilities": seraph.identity.capabilities
            },
            {
                "name": daedalus.identity.name,
                "role": daedalus.identity.role,
                "version": daedalus.identity.version,
                "capabilities": daedalus.identity.capabilities
            }
        ]
    }


@app.post("/pipeline")
def run_pipeline(request: PipelineRequest):
    """Run the full Seraph → Daedalus pipeline automatically."""
    result = coordinator.run(request.description)
    return result