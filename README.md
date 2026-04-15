# RELAY — Multi-Agent AI Platform

A multi-agent AI coordination platform where specialized agents collaborate on complex tasks. Built with Python, FastAPI, and a Next.js frontend.

**Author:** Edwin Olaez | **Course:** Emerging Trends | **Completed:** March 2026

---

## Overview

RELAY is a proof-of-concept platform that separates **planning** from **execution** across two AI agents:

- **Seraph** — strategic planning agent that decomposes tasks into ordered subtasks with success criteria
- **Daedalus** — technical execution agent equipped with tools for calculation, summarization, and more
- **GeneSys** — YAML-based identity system that gives each agent a persistent personality and constraints
- **RELAY Engine** — the message-passing coordinator that routes work between agents
- **FastAPI backend** — REST API layer that exposes the system over HTTP
- **Next.js frontend** — live interface for submitting tasks and watching agents coordinate in real time

---

## Tech Stack

| Layer          | Technology                |
| -------------- | ------------------------- |
| Language       | Python 3.11+              |
| LLM Provider   | Anthropic Claude Sonnet 4 |
| Agent Identity | GeneSys YAML documents    |
| Database       | SQLite + aiosqlite        |
| API            | FastAPI + uvicorn         |
| Frontend       | Next.js 15 + TypeScript   |

---

## Project Structure

```
relay-poc/
├── relay/
│   ├── agents/
│   │   ├── seraph.py        # Planning agent
│   │   └── daedalus.py      # Execution agent
│   ├── api/
│   │   └── main.py          # FastAPI routes
│   ├── coordinator.py       # Agent orchestration logic
│   ├── engine.py            # Message-passing engine
│   ├── genesys.py           # YAML identity loader
│   ├── db/                  # SQLite database layer
│   └── tools/               # Daedalus tool implementations
├── genesys/
│   ├── seraph.yaml          # Seraph's identity/constraints
│   └── daedalus.yaml        # Daedalus's identity/constraints
├── frontend/                # Next.js 15 app
├── tests/                   # Test suite
├── requirements.txt
└── DOCUMENTATION.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- An [Anthropic API key](https://console.anthropic.com/)

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/your-username/relay-poc.git
cd relay-poc

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Start the API server
uvicorn relay.api.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The UI will be available at `http://localhost:3000`.

---

## Evaluation Results

Tested against 5 reference tasks:

| Task                                | Agent    | Result  |
| ----------------------------------- | -------- | ------- |
| Explain single vs multi-agent AI    | Seraph   | PASS |
| Onboard a new developer plan        | Seraph   | PASS |
| Mobile app launch plan              | Seraph   | PASS |
| Calculate 12 employees x 8hrs x $25 | Daedalus | PASS |
| Calculate seconds in 30 days        | Daedalus | PASS |

**Pass Rate: 5/5 (100%)**

---

## Running Tests

```bash
pytest test_seraph.py test_daedalus.py test_genesys.py -v
```

---

## Key Concepts

- **Multi-agent coordination** — separating planning from execution across distinct agents
- **Planner-executor pattern** — Seraph thinks, Daedalus acts
- **Persistent agent identity** — YAML documents define behavior and constraints at runtime
- **Tool calling** — how AI agents invoke external capabilities like calculators
- **Async Python** — concurrent agent operations with `asyncio`
- **REST APIs** — HTTP-based communication between backend and frontend
