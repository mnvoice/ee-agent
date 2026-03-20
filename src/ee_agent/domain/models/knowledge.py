from typing import Optional, List
from pydantic import BaseModel, Field
import uuid


class Concept(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    definition: str
    subject: str
    related_formulas: List[str] = Field(default_factory=list)
    korean_terms: List[str] = Field(default_factory=list)


class Formula(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    latex: str
    description: str
    variables: dict = Field(default_factory=dict)
    applicable_subjects: List[str] = Field(default_factory=list)


class Regulation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    article: str
    content: str
    keywords: List[str] = Field(default_factory=list)


class GraphNode(BaseModel):
    node_id: str
    label: str
    properties: dict


class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    relation_type: str  # REQUIRES, APPLIES, REFERENCES, BELONGS_TO, DEPENDS_ON
    properties: dict = Field(default_factory=dict)


class RelationType:
    REQUIRES = "REQUIRES"
    APPLIES = "APPLIES"
    REFERENCES = "REFERENCES"
    BELONGS_TO = "BELONGS_TO"
    DEPENDS_ON = "DEPENDS_ON"
    HAS_TOPOLOGY = "HAS_TOPOLOGY"
