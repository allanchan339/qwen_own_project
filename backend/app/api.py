"""FastAPI application"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

from app.config import get_settings
from app.graph_engine import GraphEngine
from app.models import GraphStats, QueryRequest, QueryResult, PathResult


def create_app() -> FastAPI:
    """Create FastAPI application"""
    settings = get_settings()

    app = FastAPI(
        title="Knowledge Platform API",
        version=settings.api_version,
        debug=settings.debug,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize graph engine
    base_dir = Path(__file__).parent.parent
    graph_path = base_dir / settings.graphify_output_dir / "graph.json"
    graph_engine = GraphEngine(graph_path)

    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "name": "Knowledge Platform API",
            "version": settings.api_version,
            "status": "running",
        }

    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {"status": "healthy"}

    @app.get("/graph/stats", response_model=GraphStats)
    async def get_graph_stats():
        """Get graph statistics"""
        return graph_engine.get_stats()

    @app.get("/graph/nodes")
    async def get_nodes(limit: int = Query(100, ge=1, le=1000)):
        """Get graph nodes"""
        return graph_engine.get_nodes(limit)

    @app.get("/graph/edges")
    async def get_edges(limit: int = Query(100, ge=1, le=1000)):
        """Get graph edges"""
        return graph_engine.get_edges(limit)

    @app.get("/graph/communities")
    async def get_communities():
        """Get detected communities"""
        return graph_engine.get_communities()

    @app.get("/graph/god-nodes")
    async def get_god_nodes(top_k: int = Query(10, ge=1, le=50)):
        """Get highly connected nodes"""
        return graph_engine.get_god_nodes(top_k)

    @app.get("/graph/node/{node_id}/neighbors")
    async def get_node_neighbors(node_id: str, max_depth: int = Query(3, ge=1, le=5)):
        """Get neighbors of a node"""
        result = graph_engine.query(node_id, max_depth)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result

    @app.get("/graph/path")
    async def find_path(from_node: str, to_node: str):
        """Find shortest path between nodes"""
        result = graph_engine.find_path(from_node, to_node)
        if result is None:
            raise HTTPException(
                status_code=404, detail="No path found or nodes not found"
            )
        return result

    @app.post("/graph/extract")
    async def extract_graph(target_path: str):
        """Run graphify extraction on a target path"""
        try:
            result = graph_engine.run_graphify(Path(target_path))
            return result
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/graph/report")
    async def get_graph_report():
        """Get the graphify report"""
        report_path = (
            Path(__file__).parent.parent
            / settings.graphify_output_dir
            / "GRAPH_REPORT.md"
        )
        if not report_path.exists():
            raise HTTPException(status_code=404, detail="No report found")

        return {"report": report_path.read_text()}

    return app


app = create_app()
