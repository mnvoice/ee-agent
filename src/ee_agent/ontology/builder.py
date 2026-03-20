from pathlib import Path
from typing import Optional
from urllib.parse import quote

from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD

from ee_agent.domain.models.knowledge import Concept, Formula, Regulation
from ee_agent.domain.models.question import Question, Subject
from ee_agent.ontology.schema import EE, EEClass, EEProperty

OWL_NS = Namespace("http://www.w3.org/2002/07/owl#")

# Difficulty mapping: enum value -> integer score
_DIFFICULTY_SCORE = {"하": 1, "중": 2, "상": 3}

# Subject enum value -> EE individual URI
_SUBJECT_INDIVIDUAL = {
    Subject.ELECTRICAL_THEORY: EE.ElectricalTheory,
    Subject.ELECTRICAL_MACHINES: EE.ElectricalMachines,
    Subject.POWER_SYSTEMS: EE.PowerSystems,
    Subject.CONTROL_ENGINEERING: EE.ControlEngineering,
    Subject.ELECTRICAL_SAFETY: EE.ElectricalSafety,
    Subject.CIRCUIT_THEORY: EE.CircuitTheory,
}

_SEED_TTL = Path(__file__).parent / "ee_ontology.ttl"


class EEOntologyBuilder:
    """Builds an RDF/OWL-DL knowledge graph for the Korean EE exam domain."""

    def __init__(self) -> None:
        self.graph = Graph()
        self._bind_namespaces()
        self._load_seed_ontology()

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _bind_namespaces(self) -> None:
        self.graph.bind("ee", EE)
        self.graph.bind("owl", OWL_NS)
        self.graph.bind("rdf", RDF)
        self.graph.bind("xsd", XSD)

    def _load_seed_ontology(self) -> None:
        """Load the seed ontology TTL file into the graph."""
        if _SEED_TTL.exists():
            self.graph.parse(str(_SEED_TTL), format="turtle")
        else:
            raise FileNotFoundError(f"Seed ontology not found: {_SEED_TTL}")

    # ------------------------------------------------------------------
    # Public resource-creation methods
    # ------------------------------------------------------------------

    def add_question(self, question: Question) -> URIRef:
        """Add a Question instance as an RDF resource and return its URI."""
        uri = EE[f"question/{_safe_id(question.id)}"]
        self.graph.add((uri, RDF.type, EEClass.PROBLEM))
        self.graph.add((uri, EEProperty.QUESTION_TEXT, Literal(question.stem, datatype=XSD.string)))
        self.graph.add((uri, EEProperty.CORRECT_ANS, Literal(question.correct_answer, datatype=XSD.integer)))
        self.graph.add((uri, EEProperty.YEAR, Literal(question.year, datatype=XSD.integer)))
        difficulty_score = _DIFFICULTY_SCORE.get(question.difficulty.value, 2)
        self.graph.add((uri, EEProperty.DIFFICULTY, Literal(difficulty_score, datatype=XSD.integer)))
        return uri

    def add_concept(self, concept: Concept) -> URIRef:
        """Add a Concept instance as an RDF resource and return its URI."""
        uri = EE[f"concept/{_safe_id(concept.id)}"]
        self.graph.add((uri, RDF.type, EEClass.CONCEPT))
        self.graph.add((uri, EE.name, Literal(concept.name, datatype=XSD.string)))
        self.graph.add((uri, EE.definition, Literal(concept.definition, datatype=XSD.string)))
        self.graph.add((uri, EE.subject, Literal(concept.subject, datatype=XSD.string)))
        return uri

    def add_formula(self, formula: Formula) -> URIRef:
        """Add a Formula instance as an RDF resource and return its URI."""
        uri = EE[f"formula/{_safe_id(formula.id)}"]
        self.graph.add((uri, RDF.type, EEClass.FORMULA))
        self.graph.add((uri, EE.name, Literal(formula.name, datatype=XSD.string)))
        self.graph.add((uri, EEProperty.LATEX_EXPR, Literal(formula.latex, datatype=XSD.string)))
        self.graph.add((uri, EE.description, Literal(formula.description, datatype=XSD.string)))
        return uri

    def add_regulation(self, regulation: Regulation) -> URIRef:
        """Add a Regulation instance as an RDF resource and return its URI."""
        uri = EE[f"regulation/{_safe_id(regulation.id)}"]
        self.graph.add((uri, RDF.type, EEClass.REGULATION))
        self.graph.add((uri, EEProperty.ARTICLE_NUM, Literal(regulation.article, datatype=XSD.string)))
        self.graph.add((uri, EE.content, Literal(regulation.content, datatype=XSD.string)))
        return uri

    # ------------------------------------------------------------------
    # Linking methods
    # ------------------------------------------------------------------

    def link_question_to_concept(self, q_uri: URIRef, c_uri: URIRef) -> None:
        """Add an ee:requires triple: question → concept."""
        self.graph.add((q_uri, EEProperty.REQUIRES, c_uri))

    def link_question_to_formula(self, q_uri: URIRef, f_uri: URIRef) -> None:
        """Add an ee:applies triple: question → formula."""
        self.graph.add((q_uri, EEProperty.APPLIES, f_uri))

    def link_question_to_subject(self, q_uri: URIRef, subject: Subject) -> None:
        """Add an ee:belongsTo triple: question → subject individual."""
        subject_uri = _SUBJECT_INDIVIDUAL.get(subject)
        if subject_uri is None:
            raise ValueError(f"Unknown subject: {subject}")
        self.graph.add((q_uri, EEProperty.BELONGS_TO, subject_uri))

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def serialize_turtle(self, output_path: str) -> None:
        """Serialize the graph to a Turtle (.ttl) file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.graph.serialize(destination=str(path), format="turtle")

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_owl_dl(self) -> list[str]:
        """
        Perform lightweight OWL-DL constraint validation.

        Returns a list of violation strings.  An empty list means no
        violations were detected.

        Checks implemented:
        - Every ee:Problem must have exactly one ee:belongsTo triple.
        - Every ee:Problem must have at least one ee:requires triple.
        """
        violations: list[str] = []
        problems = list(self.graph.subjects(RDF.type, EEClass.PROBLEM))

        for prob in problems:
            prob_label = str(prob)

            # Check: exactly one belongsTo
            belongs_to = list(self.graph.objects(prob, EEProperty.BELONGS_TO))
            if len(belongs_to) == 0:
                violations.append(
                    f"OWL-DL violation: Problem <{prob_label}> has no ee:belongsTo triple "
                    f"(required: exactly 1 Subject)."
                )
            elif len(belongs_to) > 1:
                violations.append(
                    f"OWL-DL violation: Problem <{prob_label}> has {len(belongs_to)} "
                    f"ee:belongsTo triples (ee:belongsTo is Functional — max 1 allowed)."
                )

            # Check: at least one requires
            requires = list(self.graph.objects(prob, EEProperty.REQUIRES))
            if len(requires) == 0:
                violations.append(
                    f"OWL-DL violation: Problem <{prob_label}> has no ee:requires triple "
                    f"(required: min 1 Concept)."
                )

        return violations


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe_id(raw_id: str) -> str:
    """Percent-encode a raw identifier so it is safe inside a URI path segment."""
    return quote(raw_id, safe="-_.")
