"""Backend API tests"""

import pytest
from fastapi.testclient import TestClient
from app.api import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestRootEndpoints:
    """Test root and health endpoints"""

    def test_root(self, client):
        """Test root endpoint returns service info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Knowledge Platform API"
        assert "version" in data
        assert data["status"] == "running"

    def test_health(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestGraphEndpoints:
    """Test graph-related endpoints"""

    def test_graph_stats(self, client):
        """Test graph stats endpoint"""
        response = client.get("/graph/stats")
        assert response.status_code == 200
        data = response.json()
        assert "nodes" in data
        assert "edges" in data
        assert "communities" in data
        assert "average_degree" in data
        assert "density" in data

    def test_get_nodes(self, client):
        """Test get nodes endpoint"""
        response = client.get("/graph/nodes?limit=10")
        assert response.status_code == 200
        nodes = response.json()
        assert isinstance(nodes, list)
        assert len(nodes) <= 10
        if nodes:
            node = nodes[0]
            assert "id" in node
            assert "label" in node
            assert "file_type" in node
            assert "degree" in node

    def test_get_edges(self, client):
        """Test get edges endpoint"""
        response = client.get("/graph/edges?limit=10")
        assert response.status_code == 200
        edges = response.json()
        assert isinstance(edges, list)
        assert len(edges) <= 10
        if edges:
            edge = edges[0]
            assert "source" in edge
            assert "target" in edge
            assert "relation" in edge
            assert "confidence" in edge

    def test_get_communities(self, client):
        """Test get communities endpoint"""
        response = client.get("/graph/communities")
        assert response.status_code == 200
        communities = response.json()
        assert isinstance(communities, list)

    def test_get_god_nodes(self, client):
        """Test get god nodes endpoint"""
        response = client.get("/graph/god-nodes?top_k=5")
        assert response.status_code == 200
        nodes = response.json()
        assert isinstance(nodes, list)
        assert len(nodes) <= 5
        if nodes:
            node = nodes[0]
            assert "node_id" in node
            assert "label" in node
            assert "degree" in node
            assert "betweenness" in node


class TestQueryEndpoints:
    """Test query endpoints"""

    def test_node_neighbors(self, client):
        """Test node neighbors endpoint"""
        # First get a node ID
        nodes_response = client.get("/graph/nodes?limit=1")
        if nodes_response.json():
            node_id = nodes_response.json()[0]["id"]
            # URL encode the node_id (may contain special chars like /)
            from urllib.parse import quote

            encoded_id = quote(node_id, safe="")
            response = client.get(f"/graph/node/{encoded_id}/neighbors?max_depth=2")
            # Accept 200 or 404 (404 if node has no neighbors)
            assert response.status_code in [200, 404]
            if response.status_code == 200:
                data = response.json()
                assert "nodes" in data
                assert "edges" in data
        # If no nodes, skip test

    def test_find_path(self, client):
        """Test find path endpoint"""
        # Get two node IDs
        nodes_response = client.get("/graph/nodes?limit=2")
        if len(nodes_response.json()) >= 2:
            node1 = nodes_response.json()[0]["id"]
            node2 = nodes_response.json()[1]["id"]
            response = client.get(f"/graph/path?from_node={node1}&to_node={node2}")
            if response.status_code == 200:
                data = response.json()
                assert "path" in data
                assert "hops" in data
                assert "relations" in data
            # 404 is also valid if no path exists


class TestValidation:
    """Test input validation"""

    def test_nodes_limit_validation(self, client):
        """Test nodes limit validation"""
        response = client.get("/graph/nodes?limit=0")
        assert response.status_code == 422  # Validation error

        response = client.get("/graph/nodes?limit=1001")
        assert response.status_code == 422  # Validation error

    def test_god_nodes_top_k_validation(self, client):
        """Test god nodes top_k validation"""
        response = client.get("/graph/god-nodes?top_k=0")
        assert response.status_code == 422

        response = client.get("/graph/god-nodes?top_k=51")
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
