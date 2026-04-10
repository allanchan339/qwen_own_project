"""Pydantic models for the API"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class EdgeConfidence(str, Enum):
    """Edge confidence levels"""

    EXTRACTED = "EXTRACTED"
    INFERRED = "INFERRED"
    AMBIGUOUS = "AMBIGUOUS"


class Node(BaseModel):
    """Graph node representation"""

    id: str
    label: str
    file_type: str
    source_file: str
    source_location: Optional[str] = None
    degree: int = 0


class Edge(BaseModel):
    """Graph edge representation"""

    source: str
    target: str
    relation: str
    confidence: EdgeConfidence
    confidence_score: float
    weight: float = 1.0


class Community(BaseModel):
    """Community detection result"""

    id: int
    label: str
    nodes: list[str]
    cohesion: float


class GodNode(BaseModel):
    """Highly connected node"""

    node_id: str
    label: str
    degree: int
    betweenness: float


class GraphStats(BaseModel):
    """Graph statistics"""

    nodes: int
    edges: int
    communities: int
    average_degree: float
    density: float


class QueryRequest(BaseModel):
    """Semantic search request"""

    query: str
    top_k: int = 10
    include_context: bool = True


class QueryResult(BaseModel):
    """Search result"""

    node_id: str
    label: str
    score: float
    context: Optional[str] = None
    source_file: Optional[str] = None


class PathResult(BaseModel):
    """Shortest path between nodes"""

    from_node: str
    to_node: str
    path: list[str]
    hops: int
    relations: list[str]
