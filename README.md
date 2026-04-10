# Knowledge Platform

AI-powered developer knowledge platform that transforms codebases into navigable knowledge graphs.

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

### Option 1: Use the Start Script (Recommended)

```bash
./start.sh
```

This starts both backend and frontend automatically.

### Option 2: Manual Start

#### Backend

```bash
cd backend
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

uvicorn app.api:app --reload --port 8001
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000 to access the platform.

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

✅ **Backend API** - FastAPI server with graph operations (11/11 tests passing)
✅ **Frontend UI** - React dashboard with graph visualization (TypeScript: 0 errors)
✅ **Knowledge Graph** - Built from project code (66,706 nodes, 86,502 edges)
✅ **Interactive Visualization** - Force-directed graph with search
✅ **Community Detection** - Cluster analysis with cohesion scores
✅ **God Node Analysis** - Identify key concepts (optimized for large graphs)
✅ **Production Build** - Frontend builds successfully (454KB gzipped)
✅ **API Tests** - Comprehensive test suite covering all endpoints

🔄 **Future Enhancements**
- Semantic search with embeddings
- Cross-repository pattern extraction
- Auto-generated documentation

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
