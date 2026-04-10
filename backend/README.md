# Knowledge Platform Backend

AI-powered developer knowledge platform backend.

## Features

- Knowledge graph extraction using graphify
- Semantic search with vector embeddings
- Community detection and analysis
- God node identification
- Path finding between concepts

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows
pip install -e .
```

## Run

```bash
uvicorn app.api:app --reload --port 8000
```

## API Endpoints

- `GET /graph/stats` - Graph statistics
- `GET /graph/nodes` - Get nodes
- `GET /graph/edges` - Get edges  
- `GET /graph/communities` - Detected communities
- `GET /graph/god-nodes` - Highly connected nodes
- `GET /graph/node/{id}/neighbors` - Node neighbors
- `GET /graph/path` - Path between nodes
- `POST /graph/extract` - Run graphify extraction
- `GET /graph/report` - Get analysis report
