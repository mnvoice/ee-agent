import json
from pathlib import Path

from rdflib import Graph


class OntologySerializer:
    """Handles serialisation of an rdflib Graph to various RDF formats."""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def to_turtle(self, output_path: str) -> None:
        """Serialize the graph to a Turtle (.ttl) file."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        self.graph.serialize(destination=output_path, format="turtle")

    def to_json_ld(self, output_path: str) -> None:
        """Serialize the graph to a JSON-LD file."""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        self.graph.serialize(destination=output_path, format="json-ld")

    def to_string(self, fmt: str = "turtle") -> str:
        """Serialize the graph to a string in the specified format."""
        return self.graph.serialize(format=fmt)
