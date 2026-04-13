# Predly — Swarm Intelligence Prediction Engine

> **A Simple and Universal Swarm Intelligence Engine, Predicting Anything**

Predly is a next-generation AI prediction engine powered by multi-agent technology. By extracting seed information from real-world sources (breaking news, policy drafts, financial signals, literary texts), it automatically constructs a high-fidelity parallel digital world. Thousands of intelligent agents with independent personalities, long-term memory, and behavioral logic freely interact and undergo social evolution inside this sandbox. You can inject variables dynamically from a "God's-eye view" to precisely deduce future trajectories.

**Upload seed materials → describe your prediction goal → receive a detailed prediction report and a deeply interactive digital world.**

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Running Locally](#running-locally)
  - [Option A: Source Code (Recommended)](#option-a-source-code-recommended)
  - [Option B: Docker](#option-b-docker)
- [Workflow & Features](#workflow--features)
- [API Reference](#api-reference)
- [Configuration Reference](#configuration-reference)
- [Scripts](#scripts)
- [License](#license)

---

## Overview

Predly is built around a five-step pipeline:

1. **Graph Building** — Upload seed documents; the system extracts entities, relationships, and injects them into a knowledge graph (powered by Zep Cloud).
2. **Environment Setup** — Entity types are filtered and enriched; agent personas are auto-generated from the graph.
3. **Simulation** — Agents simulate dual-platform social interactions (Twitter-style & Reddit-style) with dynamic temporal memory updates.
4. **Report Generation** — A dedicated `ReportAgent` with a rich toolset queries the post-simulation world and produces a structured prediction report.
5. **Deep Interaction** — Chat with any individual agent in the simulated world, or continue a dialogue with the ReportAgent.

### Use Cases

- **Policy & PR rehearsal** — Test how a policy or announcement ripples through a population before release.
- **Public opinion prediction** — Simulate social media reactions to news events.
- **Creative exploration** — Deduce fictional story endings (e.g., literary "lost chapter" reconstruction).
- **Financial & political scenarios** — Model crowd reactions to financial signals or electoral events.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Vue 3 Frontend                      │
│  Home → Step1(Graph) → Step2(Env) → Step3(Sim) →        │
│         Step4(Report) → Step5(Interaction)              │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP (axios)
┌────────────────────────▼────────────────────────────────┐
│               Flask Backend  :5001                      │
│                                                         │
│  /api/graph/*        Graph & Ontology routes            │
│  /api/simulation/*   Simulation & Entity routes         │
│  /api/report/*       Report Agent routes                │
│                                                         │
│  Services:                                              │
│  ├── OntologyGenerator      (LLM → entity/edge schema)  │
│  ├── GraphBuilderService    (Zep Cloud graph creation)  │
│  ├── ZepEntityReader        (entity/relationship fetch) │
│  ├── OasisProfileGenerator  (agent persona generation)  │
│  ├── SimulationManager      (orchestration & state)     │
│  ├── SimulationRunner       (OASIS engine execution)    │
│  ├── ReportAgent            (post-sim analysis & chat)  │
│  └── ZepGraphMemoryUpdater  (live memory updates)       │
└───────────┬─────────────────────────┬───────────────────┘
            │                         │
  ┌─────────▼──────────┐   ┌──────────▼──────────────┐
  │    Zep Cloud        │   │   OASIS Simulation       │
  │  (Graph Memory)     │   │  (camel-oasis engine)    │
  └────────────────────┘   └─────────────────────────┘
            │
  ┌─────────▼──────────┐
  │   LLM Providers     │
  │  Primary: Groq      │
  │  Boost:   Gemini    │
  └────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Vue 3, Vue Router 4, Vite, Axios, D3.js |
| **Backend** | Python 3.11–3.12, Flask 3, Flask-CORS |
| **LLM Client** | OpenAI SDK (provider-agnostic) — Groq / Gemini / Qwen / any OpenAI-compatible API |
| **Graph Memory** | Zep Cloud (`zep-cloud 3.13.0`) |
| **Simulation Engine** | OASIS (`camel-oasis 0.2.5`, `camel-ai 0.2.78`) |
| **File Parsing** | PyMuPDF (PDF), charset-normalizer / chardet (text encoding) |
| **Data Validation** | Pydantic v2 |
| **Package Manager (Python)** | `uv` |
| **Package Manager (JS)** | npm |
| **Containerisation** | Docker / Docker Compose |

---

## Project Structure

```
Predly-API-main/
├── .env.example                  # Environment variable template
├── docker-compose.yml            # Docker deployment
├── Dockerfile
├── package.json                  # Root npm scripts (dev, setup, build)
│
├── frontend/                     # Vue 3 SPA
│   ├── src/
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   ├── MainView.vue      # Step 1–4 container
│   │   │   ├── SimulationView.vue
│   │   │   ├── ReportView.vue
│   │   │   └── InteractionView.vue
│   │   ├── components/
│   │   │   ├── Step1GraphBuild.vue
│   │   │   ├── Step2EnvSetup.vue
│   │   │   ├── Step3Simulation.vue
│   │   │   ├── Step4Report.vue
│   │   │   └── Step5Interaction.vue
│   │   ├── api.js                # Axios API client
│   │   └── router/index.js
│   └── vite.config.js
│
└── backend/
    ├── run.py                    # Flask entry point (port 5001)
    ├── requirements.txt
    ├── pyproject.toml
    └── app/
        ├── config.py             # All config loaded from .env
        ├── api/
        │   ├── graph.py          # /api/graph/* endpoints
        │   ├── simulation.py     # /api/simulation/* endpoints
        │   └── report.py         # /api/report/* endpoints
        ├── models/
        │   ├── project.py        # ProjectManager, ProjectStatus
        │   └── task.py           # TaskManager, TaskStatus
        ├── services/
        │   ├── ontology_generator.py        # LLM → ontology schema
        │   ├── graph_builder.py             # Zep graph CRUD
        │   ├── text_processor.py            # Chunking & preprocessing
        │   ├── zep_entity_reader.py         # Entity/edge retrieval
        │   ├── zep_graph_memory_updater.py  # Live graph updates
        │   ├── zep_tools.py                 # Zep utility functions
        │   ├── oasis_profile_generator.py   # Agent persona generation
        │   ├── simulation_config_generator.py
        │   ├── simulation_manager.py        # Simulation lifecycle
        │   ├── simulation_runner.py         # OASIS execution
        │   ├── simulation_ipc.py            # Inter-process comms
        │   └── report_agent.py              # Post-sim report & chat
        └── utils/
            ├── llm_client.py      # Multi-key rotating LLM client
            ├── file_parser.py     # PDF / MD / TXT extraction
            ├── logger.py
            ├── retry.py
            └── zep_paging.py
```

---

## Environment Variables

Copy the example file and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `LLM_API_KEY` / `LLM_API_KEY_1` | ✅ | Primary LLM API key (Groq, Qwen, or any OpenAI-compatible provider) |
| `LLM_API_KEY_2`, `LLM_API_KEY_3`, `LLM_API_KEY_4` | ➖ | Additional primary keys — auto-rotated on rate limit |
| `LLM_BASE_URL` | ✅ | Base URL of the primary LLM provider |
| `LLM_MODEL_NAME` | ✅ | Model name for the primary LLM |
| `ZEP_API_KEY` | ✅ | Zep Cloud API key — free tier sufficient for basic usage |
| `LLM_BOOST_API_KEY_1/2/3` | ➖ | Boost LLM keys (e.g. Gemini) for heavier reasoning tasks |
| `LLM_BOOST_BASE_URL` | ➖ | Base URL for boost LLM |
| `LLM_BOOST_MODEL_NAME` | ➖ | Model name for boost LLM (e.g. `gemini-2.5-flash`) |
| `OASIS_DEFAULT_MAX_ROUNDS` | ➖ | Max simulation rounds (default: `3`; keep low to avoid token overflow) |
| `REPORT_AGENT_MAX_TOOL_CALLS` | ➖ | Tool call budget per report agent turn (default: `1`) |
| `REPORT_AGENT_MAX_REFLECTION_ROUNDS` | ➖ | Reflection depth of report agent (default: `1`) |
| `REPORT_AGENT_TEMPERATURE` | ➖ | Temperature for report generation (default: `0.3`) |

### Recommended Free-Tier Setup

- **Primary LLM**: [Groq](https://console.groq.com/) — use `meta-llama/llama-4-scout-17b-16e-instruct` or similar
- **Boost LLM**: [Google AI Studio](https://aistudio.google.com/) — `gemini-2.5-flash` (generous free quota)
- **Graph Memory**: [Zep Cloud](https://app.getzep.com/) — free monthly quota covers simple simulations

Alternatively, use Alibaba's [Bailian Platform](https://bailian.console.aliyun.com/) with `qwen-plus` for both primary and boost.

---

## Running Locally

### Prerequisites

| Tool | Version | Check |
|---|---|---|
| Node.js | ≥ 18 | `node -v` |
| Python | ≥ 3.11, ≤ 3.12 | `python --version` |
| uv | Latest | `uv --version` |

Install `uv` if you don't have it:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

### Option A: Source Code (Recommended)

#### Step 1 — Clone & configure

```bash
git clone https://github.com/666ghj/Predly.git
cd Predly

# Copy and fill in environment variables
cp .env.example .env
# Edit .env — at minimum set LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME, ZEP_API_KEY
```

#### Step 2 — Install all dependencies (one command)

```bash
npm run setup:all
```

This installs:
- Root Node.js dependencies (`concurrently`)
- Frontend Node.js dependencies (Vue 3, Vite, Axios, D3)
- Backend Python dependencies via `uv` (Flask, OpenAI SDK, camel-oasis, Zep, PyMuPDF, etc.)

Or install step by step:

```bash
npm run setup          # Node deps (root + frontend)
npm run setup:backend  # Python deps (creates venv automatically via uv)
```

#### Step 3 — Start both servers

```bash
npm run dev
```

This concurrently starts:

| Service | URL |
|---|---|
| **Frontend** (Vue / Vite dev server) | http://localhost:3000 |
| **Backend** (Flask API) | http://localhost:5001 |

#### Start services individually

```bash
npm run backend    # Flask backend only
npm run frontend   # Vite frontend only
```

---

### Option B: Docker

```bash
# 1. Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# 2. Pull image and start
docker compose up -d
```

The container exposes:
- Port `3000` — Frontend
- Port `10000` — Backend API (mapped from internal 5001)

Uploaded files are persisted via a volume mount at `./backend/uploads`.

To stop:

```bash
docker compose down
```

> If image pull is slow, the `docker-compose.yml` includes a comment with a mirror address — swap the image line as instructed.

---

## Workflow & Features

### Step 1 — Graph Building

- Upload seed documents in **PDF, MD, or TXT** format (up to 50 MB total)
- Describe your simulation goal in natural language
- The system calls the LLM to generate an **ontology** (entity types + relationship types) tailored to your documents
- Text is chunked and injected into a **Zep Cloud knowledge graph** in batches
- Progress is tracked asynchronously via a task polling endpoint

### Step 2 — Environment Setup

- Entity nodes are fetched and filtered from the graph
- Relationship edges are enriched per entity
- **Agent personas** are auto-generated by the LLM from graph data (background, personality, behavioral tendencies)
- Simulation configuration is prepared for the OASIS engine

### Step 3 — Simulation

- Dual-platform parallel simulation:
  - **Twitter-style** actions: `CREATE_POST`, `LIKE_POST`, `REPOST`, `FOLLOW`, `DO_NOTHING`, `QUOTE_POST`
  - **Reddit-style** actions: `LIKE_POST`, `DISLIKE_POST`, `CREATE_POST`, `CREATE_COMMENT`, `SEARCH_POSTS`, `TREND`, `FOLLOW`, `MUTE`, and more
- Simulation rounds are configurable via `OASIS_DEFAULT_MAX_ROUNDS`
- Agents maintain long-term memory via Zep; memory is updated dynamically each round
- Simulation data is saved to `backend/uploads/simulations/`

### Step 4 — Report Generation

- A **ReportAgent** with a rich toolset queries the post-simulation Zep graph
- Performs deep analysis and produces a structured prediction report
- Configurable via `REPORT_AGENT_MAX_TOOL_CALLS`, `REPORT_AGENT_MAX_REFLECTION_ROUNDS`, and `REPORT_AGENT_TEMPERATURE`

### Step 5 — Deep Interaction

- **Interview any agent**: Chat directly with a specific simulated agent; responses are grounded in their persona and full memory history
- **Chat with ReportAgent**: Continue questioning the report agent to drill deeper into specific findings
- Interview prompts are automatically prefixed to prevent tool invocation and ensure direct conversational replies

---

## API Reference

All endpoints are served at `http://localhost:5001`.

### Graph Endpoints (`/api/graph`)

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/graph/ontology/generate` | Upload files + generate ontology schema |
| `POST` | `/api/graph/build` | Build Zep knowledge graph from project |
| `GET` | `/api/graph/task/<task_id>` | Poll async task status |
| `GET` | `/api/graph/tasks` | List all tasks |
| `GET` | `/api/graph/project/<project_id>` | Get project details |
| `GET` | `/api/graph/project/list` | List all projects |
| `DELETE` | `/api/graph/project/<project_id>` | Delete a project |
| `POST` | `/api/graph/project/<project_id>/reset` | Reset project to rebuild graph |
| `GET` | `/api/graph/data/<graph_id>` | Fetch graph nodes and edges |
| `DELETE` | `/api/graph/delete/<graph_id>` | Delete a Zep graph |

### Simulation Endpoints (`/api/simulation`)

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/simulation/entities/<graph_id>` | Get filtered entities from graph |
| `POST` | `/api/simulation/profiles/generate` | Generate agent personas |
| `POST` | `/api/simulation/run` | Start simulation |
| `GET` | `/api/simulation/status/<sim_id>` | Poll simulation status |
| `POST` | `/api/simulation/interview` | Interview a specific agent |

### Report Endpoints (`/api/report`)

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/report/generate` | Generate prediction report |
| `POST` | `/api/report/chat` | Chat with ReportAgent |

---

## Configuration Reference

All runtime configuration lives in `backend/app/config.py` and is sourced from `.env`.

| Config Key | Default | Notes |
|---|---|---|
| `MAX_CONTENT_LENGTH` | 50 MB | Max upload size |
| `ALLOWED_EXTENSIONS` | `pdf, md, txt, markdown` | Accepted file types |
| `DEFAULT_CHUNK_SIZE` | 500 | Characters per text chunk |
| `DEFAULT_CHUNK_OVERLAP` | 50 | Overlap between chunks |
| `OASIS_DEFAULT_MAX_ROUNDS` | 3 | Simulation rounds (keep ≤ 40 for cost control) |
| `REPORT_AGENT_MAX_TOOL_CALLS` | 1 | Tool calls per agent turn |
| `REPORT_AGENT_MAX_REFLECTION_ROUNDS` | 1 | Agent reflection depth |
| `REPORT_AGENT_TEMPERATURE` | 0.3 | Report LLM temperature |

The LLM client supports **automatic key rotation**: if a rate limit is hit on one key, the next configured key in the list is used transparently.

---

## Scripts

Standalone simulation scripts are available in `backend/scripts/`:

| Script | Description |
|---|---|
| `run_twitter_simulation.py` | Run a standalone Twitter-style simulation |
| `run_reddit_simulation.py` | Run a standalone Reddit-style simulation |
| `run_parallel_simulation.py` | Run both platforms in parallel |
| `action_logger.py` | Log and inspect agent actions |
| `test_profile_format.py` | Validate generated agent profile format |

Run them with:

```bash
cd backend
uv run python scripts/run_twitter_simulation.py
```

---

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

Predly's simulation engine is powered by **[OASIS (Open Agent Social Interaction Simulations)](https://github.com/camel-ai/oasis)** by the CAMEL-AI team. Predly has received strategic support and incubation from **[Shanda Group](https://www.shanda.com/)**.
