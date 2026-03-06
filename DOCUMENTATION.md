# RELAY Multi-Agent Platform

## Implementation Documentation

**Author:** Edwin Olaez  
**Course:** Emerging Trends  
**Completion Date:** March 2026

---

## What I Built

RELAY is a multi-agent AI coordination platform where two specialized
AI agents collaborate on complex tasks:

- **Seraph** — a strategic planning agent that decomposes tasks into
  ordered subtasks with success criteria
- **Daedalus** — a technical execution agent with tools for calculation,
  summarization, and more
- **GeneSys** — a YAML-based identity system that gives each agent
  persistent personality and constraints
- **RELAY Engine** — the message-passing coordinator between agents
- **FastAPI** — a real API layer that exposes the system to the web
- **Next.js Frontend** — a live interface for submitting tasks and
  watching agents coordinate

---

## Technology Stack

| Layer          | Technology                |
| -------------- | ------------------------- |
| Language       | Python 3.11+              |
| LLM Provider   | Anthropic Claude Sonnet 4 |
| Agent Identity | GeneSys YAML documents    |
| Database       | SQLite + aiosqlite        |
| API            | FastAPI + uvicorn         |
| Frontend       | Next.js 15 + TypeScript   |

---

## Evaluation Results

Tested against 5 reference tasks on March 2026:

| Task                                | Agent    | Result  |
| ----------------------------------- | -------- | ------- |
| Explain single vs multi-agent AI    | Seraph   | ✅ PASS |
| Onboard a new developer plan        | Seraph   | ✅ PASS |
| Mobile app launch plan              | Seraph   | ✅ PASS |
| Calculate 12 employees × 8hrs × $25 | Daedalus | ✅ PASS |
| Calculate seconds in 30 days        | Daedalus | ✅ PASS |

**Pass Rate: 5/5 (100%)**

---

## What I Learned

[Write 3-5 sentences in your own words here]
Example topics to cover:

- What surprised you most about building this?
- What was harder than you expected?
- What clicked that didn't make sense before?

---

## What I Would Do Next

[Write 2-3 things you would add or improve]
Example ideas:

- Connect Seraph and Daedalus automatically end-to-end
- Add a web_search tool so Daedalus can look things up online
- Add more agents with different specializations

---

## Key Concepts Learned

- **Multi-agent coordination** — separating planning from execution
- **Planner-executor pattern** — Seraph thinks, Daedalus acts
- **Persistent agent identity** — YAML documents define agent behavior
- **REST APIs** — how systems communicate over HTTP
- **Async Python** — running concurrent operations
- **Tool calling** — how AI agents use external capabilities
