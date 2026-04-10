"""Build knowledge graph from Python code using AST"""

import ast
import json
import networkx as nx
from pathlib import Path
from typing import Any
from networkx.readwrite import json_graph


class CodeGraphBuilder:
    """Build knowledge graph from Python source code"""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.G = nx.Graph()

    def extract_python_file(self, file_path: Path) -> dict[str, Any]:
        """Extract AST-based graph from a Python file"""
        try:
            source = file_path.read_text()
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError) as e:
            return {"nodes": [], "edges": []}

        nodes = []
        edges = []
        relative_path = str(file_path.relative_to(self.base_path))

        # Extract classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_id = f"{relative_path}_{node.name}"
                nodes.append(
                    {
                        "id": class_id,
                        "label": node.name,
                        "file_type": "code",
                        "source_file": relative_path,
                        "source_location": f"line {node.lineno}",
                        "type": "class",
                    }
                )

                # Add base classes
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        edges.append(
                            {
                                "source": class_id,
                                "target": f"{relative_path}_{base.id}",
                                "relation": "inherits",
                                "confidence": "EXTRACTED",
                                "confidence_score": 1.0,
                                "weight": 1.0,
                            }
                        )

                # Add methods as children
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_id = f"{class_id}_{item.name}"
                        nodes.append(
                            {
                                "id": method_id,
                                "label": f"{node.name}.{item.name}",
                                "file_type": "code",
                                "source_file": relative_path,
                                "source_location": f"line {item.lineno}",
                                "type": "method",
                            }
                        )
                        edges.append(
                            {
                                "source": class_id,
                                "target": method_id,
                                "relation": "contains",
                                "confidence": "EXTRACTED",
                                "confidence_score": 1.0,
                                "weight": 1.0,
                            }
                        )

            elif isinstance(node, ast.FunctionDef):
                func_id = f"{relative_path}_{node.name}"
                nodes.append(
                    {
                        "id": func_id,
                        "label": node.name,
                        "file_type": "code",
                        "source_file": relative_path,
                        "source_location": f"line {node.lineno}",
                        "type": "function",
                    }
                )

                # Track function calls
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name):
                            call_id = f"{relative_path}_{child.func.id}"
                            edges.append(
                                {
                                    "source": func_id,
                                    "target": call_id,
                                    "relation": "calls",
                                    "confidence": "EXTRACTED",
                                    "confidence_score": 1.0,
                                    "weight": 1.0,
                                }
                            )
                        elif isinstance(child.func, ast.Attribute):
                            # Method calls like obj.method()
                            method_name = child.func.attr
                            if hasattr(child.func.value, "id"):
                                target_id = f"{relative_path}_{child.func.value.id}_{method_name}"
                                edges.append(
                                    {
                                        "source": func_id,
                                        "target": target_id,
                                        "relation": "calls",
                                        "confidence": "EXTRACTED",
                                        "confidence_score": 1.0,
                                        "weight": 1.0,
                                    }
                                )

            # Track imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    import_id = f"{relative_path}_import_{alias.name}"
                    nodes.append(
                        {
                            "id": import_id,
                            "label": f"import {alias.name}",
                            "file_type": "code",
                            "source_file": relative_path,
                            "source_location": f"line {node.lineno}",
                            "type": "import",
                        }
                    )

            elif isinstance(node, ast.ImportFrom):
                import_id = f"{relative_path}_from_{node.module}"
                nodes.append(
                    {
                        "id": import_id,
                        "label": f"from {node.module}",
                        "file_type": "code",
                        "source_file": relative_path,
                        "source_location": f"line {node.lineno}",
                        "type": "import",
                    }
                )

        return {"nodes": nodes, "edges": edges}

    def build_from_directory(self, directory: Path) -> None:
        """Build graph from all Python files in directory"""
        for py_file in directory.rglob("*.py"):
            relative = py_file.relative_to(self.base_path)
            print(f"Processing: {relative}")

            result = self.extract_python_file(py_file)

            # Add nodes
            for node in result["nodes"]:
                self.G.add_node(node["id"], **node)

            # Add edges
            for edge in result["edges"]:
                self.G.add_edge(edge["source"], edge["target"], **edge)

    def add_file_nodes(self) -> None:
        """Add file-level nodes for better structure"""
        for py_file in self.base_path.rglob("*.py"):
            file_id = str(py_file.relative_to(self.base_path))
            self.G.add_node(
                file_id,
                label=f"File: {file_id}",
                file_type="file",
                source_file=file_id,
                source_location=None,
                type="file",
            )

            # Connect to functions/classes in file
            for node_id, data in self.G.nodes(data=True):
                if data.get("source_file") == file_id and data.get("type") in [
                    "class",
                    "function",
                ]:
                    self.G.add_edge(
                        file_id,
                        node_id,
                        relation="contains",
                        confidence="EXTRACTED",
                        confidence_score=1.0,
                        weight=1.0,
                    )

    def save(self, output_path: Path) -> None:
        """Save graph to JSON file"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = json_graph.node_link_data(self.G, edges="links")
        output_path.write_text(json.dumps(data, indent=2))

        print(f"Saved graph: {output_path}")
        print(f"  Nodes: {self.G.number_of_nodes()}")
        print(f"  Edges: {self.G.number_of_edges()}")

    def get_stats(self) -> dict[str, Any]:
        """Get graph statistics"""
        return {
            "nodes": self.G.number_of_nodes(),
            "edges": self.G.number_of_edges(),
            "average_degree": sum(d for _, d in self.G.degree())
            / max(1, self.G.number_of_nodes()),
            "density": self.G.number_of_edges()
            / max(1, self.G.number_of_nodes() * (self.G.number_of_nodes() - 1) / 2),
        }


def build_graph(project_path: Path, output_path: Path) -> dict[str, Any]:
    """Build knowledge graph for a project"""
    print(f"Building graph for: {project_path}")

    builder = CodeGraphBuilder(project_path)
    builder.build_from_directory(project_path)
    builder.add_file_nodes()
    builder.save(output_path)

    return builder.get_stats()


if __name__ == "__main__":
    import sys

    project = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    output = Path("graphify-out/graph.json")
    stats = build_graph(project, output)
    print(f"Stats: {stats}")
