# Knowledge Platform
AI-powered developer knowledge platform that transforms codebases into navigable knowledge graphs.
<img width="1655" height="917" alt="image" src="https://github.com/user-attachments/assets/5e399705-6100-41f7-a23f-b51919b1902c" />

> 💰 **Development Cost:** 138.2k tokens over 1h 9m - [View conversation log](log.md)

## Background of this project
This was a stability test for Qwen3.5-27B for tool calling, long context agentic work, and reasoning ability. 

### Why this test matter
This is a test to see if my hardware will drift the model output (mixed GPUs, see https://github.com/allanchan339/vllm-qwen3.5-27B for details) and error introduced due to quantization. Also, tool calling issue is a unsolved problem that hidder self-hosted LLM user reliably to do agentic work. A [reddit post](https://www.reddit.com/r/LocalLLaMA/comments/1sdhvc5/qwen_35_tool_calling_fixes_for_agentic_use_whats/) dissued this. Apart from it, numbers of PR is pending to merge in vllm, sglang, or llama.cpp e.g. https://github.com/QwenLM/Qwen3/issues/1831, https://github.com/vllm-project/vllm/issues/38885, https://github.com/vllm-project/vllm/pull/38996, https://github.com/vllm-project/vllm/pull/33965, https://github.com/vllm-project/vllm/issues/35266, and etc.


### Hardware setting
- RTX 3090 24GB (SM80)
- RTX 4090 24GB (SM89)

Mixing hardware is never be a good idea as even a small calculation different in awq_marlin and propagate error in causal LM (looping will drift the error even bigger and thus collapse the conversation session), see https://github.com/vllm-project/vllm/issues/34437 for detail. But these cards are all i have. 

### Testing Environment
- vllm=0.19.0
- transformers=5.5
- cuda=12.8
- opencode 1.3.17 with [graphify](https://github.com/safishamsi/graphify) 0.3.12 and [oh-my-opencode-slim](https://github.com/alvinunreal/oh-my-opencode-slim) 0.9.5

To perform this test, I ask this LLM to build whatever he want with $10000 token budget. Surprisingly once LLM start to run, it is unstopped for 18mins. Therefore, I decided to help him by providing issue i see. This repo is what he build eventually. 
<img width="1066" height="1235" alt="image" src="https://github.com/user-attachments/assets/df9fcee3-cc99-432c-9a4b-426a150883b4" />

## Features

- 🧠 **Knowledge Graph Extraction** - Automatically extract entities, relationships, and patterns from code
- 🔍 **Semantic Search** - Find related concepts across your entire codebase
- 📊 **Community Detection** - Discover natural clusters and architecture patterns
- 🎯 **God Node Analysis** - Identify highly connected concepts that bridge multiple areas
- 📈 **Interactive Visualization** - Explore your codebase as an interactive graph
- 📝 **Auto-generated Reports** - Comprehensive analysis with actionable insights

## Architecture

```
knowledge-platform/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api.py       # API endpoints
│   │   ├── config.py    # Configuration
│   │   ├── models.py    # Pydantic models
│   │   ├── graph_engine.py  # Graph operations
│   │   └── main.py      # Entry point
│   └── pyproject.toml
├── frontend/            # React frontend
│   ├── src/
│   │   ├── pages/       # Page components
│   │   ├── components/  # Reusable components
│   │   ├── hooks/       # Custom React hooks
│   │   └── lib/         # API client
│   └── package.json
└── graphify-out/        # Generated knowledge graph
```

## Quick Start

### Single Command Start (Recommended)

```bash
./start.sh
```

This starts a unified server that serves both the frontend and backend API on port 8080.

### Manual Start

```bash
cd backend
source .venv/bin/activate
uvicorn app.api:app --reload --port 8080
```

Visit http://localhost:8080 to access the platform.

**Note:** The frontend must be built once before first use:
```bash
cd frontend
npm install
npm run build
```

## Usage

### 1. Run Graphify Extraction

Point the platform at a codebase to extract the knowledge graph:

```bash
# From the project root
graphify /path/to/codebase

# Or via API
POST /api/graph/extract
{
  "target_path": "/path/to/codebase"
}
```

### 2. Explore the Dashboard

- **Dashboard** - Overview of graph statistics and key insights
- **Graph View** - Interactive visualization with search and exploration
- **Communities** - Detected clusters with cohesion scores
- **Report** - Full analysis report with god nodes and surprising connections

### 3. Query the Graph

- Search for specific nodes
- Find shortest paths between concepts
- Explore node neighborhoods
- Identify cross-community connections

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/graph/stats` | GET | Graph statistics |
| `/graph/nodes` | GET | Get nodes with degree |
| `/graph/edges` | GET | Get edges with confidence |
| `/graph/communities` | GET | Detected communities |
| `/graph/god-nodes` | GET | Highly connected nodes |
| `/graph/node/{id}/neighbors` | GET | Node neighbors (BFS) |
| `/graph/path` | GET | Shortest path between nodes |
| `/graph/extract` | POST | Run graphify extraction |
| `/graph/report` | GET | Get analysis report |

## Tech Stack

- **Backend**: Python, FastAPI, Pydantic, NetworkX
- **Frontend**: React, TypeScript, TailwindCSS, ForceGraph2D
- **Graph Engine**: Custom AST-based Python graph builder
- **State**: TanStack Query

## Current Status

✅ **Unified Server** - Single FastAPI server serving both frontend & API (port 8080)
✅ **Backend API** - All 11 tests passing
✅ **Frontend UI** - React dashboard (TypeScript: 0 errors)
✅ **Knowledge Graph** - 66,706 nodes, 86,502 edges extracted
✅ **Interactive Visualization** - Force-directed graph with search
✅ **Community Detection** - Cluster analysis with cohesion scores
✅ **God Node Analysis** - Optimized for large graphs (degree-based ranking)
✅ **Production Ready** - Frontend built (454KB JS, 15KB CSS)

## Architecture

**Single Server Design:**
- FastAPI serves both frontend static files and API endpoints
- No separate frontend dev server needed
- Simplified deployment: one process, one port
- SPA routing handled by FastAPI fallback

## Development

### Backend Development

```bash
cd backend
pip install -e ".[dev]"
pytest
```

### Frontend Development

```bash
cd frontend
npm run dev
```

## License

MIT
