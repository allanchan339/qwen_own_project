"""Graph engine for knowledge graph operations"""

import json
import subprocess
from pathlib import Path
from typing import Any
import networkx as nx
from networkx.readwrite import json_graph

from app.models import Node, Edge, Community, GodNode, GraphStats, PathResult


class GraphEngine:
    """Engine for graph operations"""

    def __init__(self, graph_path: Path):
        self.graph_path = graph_path
        self.G: nx.Graph | None = None
        self.communities: dict[int, list[str]] = {}
        self._load_graph()

    def reload(self) -> None:
        """Reload graph from disk"""
        self._load_graph()

    def _load_graph(self) -> None:
        """Load graph from JSON file"""
        if not self.graph_path.exists():
            self.G = nx.Graph()
            return

        data = json.loads(self.graph_path.read_text())
        self.G = json_graph.node_link_graph(data, edges="links")

        # Load communities if available
        metadata_path = self.graph_path.parent / "graph_metadata.json"
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text())
            self.communities = {
                int(k): v for k, v in metadata.get("communities", {}).items()
            }

    def run_graphify(self, target_path: Path, mode: str = "standard") -> dict[str, Any]:
        """Run graphify extraction on a target path"""
        cmd = ["graphify", str(target_path)]
        if mode == "deep":
            cmd.append("--mode")
            cmd.append("deep")

        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=str(target_path)
        )

        if result.returncode != 0:
            raise RuntimeError(f"Graphify failed: {result.stderr}")

        # Reload graph after extraction
        self._load_graph()

        return {"status": "success", "output": result.stdout}

    def get_stats(self) -> GraphStats:
        """Get graph statistics"""
        if not self.G or self.G.number_of_nodes() == 0:
            return GraphStats(
                nodes=0, edges=0, communities=0, average_degree=0.0, density=0.0
            )

        num_nodes = self.G.number_of_nodes()
        num_edges = self.G.number_of_edges()

        # Calculate average degree
        degrees = [d for _, d in self.G.degree()]
        avg_degree = sum(degrees) / num_nodes if num_nodes > 0 else 0

        # Calculate density
        max_edges = num_nodes * (num_nodes - 1) / 2
        density = num_edges / max_edges if max_edges > 0 else 0

        return GraphStats(
            nodes=num_nodes,
            edges=num_edges,
            communities=len(self.communities),
            average_degree=avg_degree,
            density=density,
        )

    def get_nodes(self, limit: int = 100) -> list[Node]:
        """Get nodes with their degree"""
        nodes = []
        for node_id, data in self.G.nodes(data=True):
            degree = self.G.degree(node_id)
            nodes.append(
                Node(
                    id=node_id,
                    label=data.get("label", node_id),
                    file_type=data.get("file_type", "unknown"),
                    source_file=data.get("source_file", ""),
                    source_location=data.get("source_location"),
                    degree=degree,
                )
            )

        # Sort by degree and return top N
        nodes.sort(key=lambda n: n.degree, reverse=True)
        return nodes[:limit]

    def get_edges(self, limit: int = 100) -> list[Edge]:
        """Get edges with confidence scores"""
        edges = []
        for source, target, data in self.G.edges(data=True):
            edges.append(
                Edge(
                    source=source,
                    target=target,
                    relation=data.get("relation", ""),
                    confidence=data.get("confidence", "AMBIGUOUS"),
                    confidence_score=data.get("confidence_score", 0.5),
                    weight=data.get("weight", 1.0),
                )
            )

        # Sort by confidence score
        edges.sort(key=lambda e: e.confidence_score, reverse=True)
        return edges[:limit]

    def get_communities(self) -> list[Community]:
        """Get detected communities"""
        communities = []
        for comm_id, nodes in self.communities.items():
            # Calculate cohesion (internal edges / total possible edges)
            subgraph = self.G.subgraph(nodes) if self.G else nx.Graph()
            num_nodes = len(nodes)
            num_edges = subgraph.number_of_edges()
            max_edges = num_nodes * (num_nodes - 1) / 2
            cohesion = num_edges / max_edges if max_edges > 0 else 0

            communities.append(
                Community(
                    id=comm_id,
                    label=f"Community {comm_id}",
                    nodes=nodes,
                    cohesion=cohesion,
                )
            )

        return communities

    def get_god_nodes(self, top_k: int = 10) -> list[GodNode]:
        """Get highly connected nodes (god nodes) - optimized for large graphs"""
        if not self.G:
            return []

        # For large graphs, use degree-based ranking (O(n log n)) instead of betweenness (O(nm))
        # This is much faster and still identifies important nodes
        sorted_by_degree = sorted(
            self.G.nodes(data=True), key=lambda x: self.G.degree(x[0]), reverse=True
        )

        god_nodes = []
        for node_id, data in sorted_by_degree:
            degree = self.G.degree(node_id)
            # Use degree as a proxy - normalized by max degree in graph
            max_degree = (
                max(self.G.degree(n) for n in self.G.nodes())
                if self.G.number_of_nodes() > 0
                else 1
            )
            betweenness_proxy = degree / max_degree if max_degree > 0 else 0

            god_nodes.append(
                GodNode(
                    node_id=node_id,
                    label=data.get("label", node_id),
                    degree=degree,
                    betweenness=betweenness_proxy,
                )
            )

            if len(god_nodes) >= top_k:
                break

        return god_nodes

    def find_path(self, from_node: str, to_node: str) -> PathResult | None:
        """Find shortest path between two nodes"""
        if not self.G:
            return None

        try:
            path = nx.shortest_path(self.G, from_node, to_node)

            # Get relations along the path
            relations = []
            for i in range(len(path) - 1):
                edge_data = self.G.edges[path[i], path[i + 1]]
                relations.append(edge_data.get("relation", ""))

            return PathResult(
                from_node=from_node,
                to_node=to_node,
                path=path,
                hops=len(path) - 1,
                relations=relations,
            )
        except nx.NetworkXNoPath:
            return None
        except nx.NodeNotFound:
            return None

    def query(self, query_node: str, max_depth: int = 3) -> dict[str, Any]:
        """BFS query from a starting node"""
        if not self.G or query_node not in self.G:
            return {"error": "Node not found"}

        visited = {query_node}
        frontier = [query_node]
        result = {"nodes": [], "edges": [], "depths": {}}

        for depth in range(max_depth):
            next_frontier = []
            for node in frontier:
                result["nodes"].append(
                    {
                        "id": node,
                        "label": self.G.nodes[node].get("label", node),
                        "depth": depth,
                    }
                )
                result["depths"][node] = depth

                for neighbor in self.G.neighbors(node):
                    if neighbor not in visited:
                        next_frontier.append(neighbor)
                        visited.add(neighbor)
                        result["edges"].append(
                            {
                                "source": node,
                                "target": neighbor,
                                "relation": self.G.edges[node, neighbor].get(
                                    "relation", ""
                                ),
                            }
                        )

            frontier = next_frontier
            if not frontier:
                break

        return result
