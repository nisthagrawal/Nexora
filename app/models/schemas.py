from __future__ import annotations

from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class Outcome(str, Enum):
    LOW = "LOW RISK"
    REVIEW = "REVIEW REQUIRED"
    HIGH = "HIGH RISK"


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class Evidence(BaseModel):
    module: str
    kind: str = "observation"
    field: str | None = None
    value: Any | None = None
    confidence: float = Field(ge=0, le=1)
    severity: float = Field(default=0, ge=0, le=1)
    region: BoundingBox | None = None
    explanation: str


class ModuleResult(BaseModel):
    module_name: str
    status: str
    confidence: float = Field(ge=0, le=1)
    evidence: list[Evidence] = Field(default_factory=list)
    affected_field: str | None = None
    affected_region: BoundingBox | None = None
    explanation: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class Contradiction(BaseModel):
    field: str
    values: list[Any]
    sources: list[str]
    severity: float
    explanation: str


class RiskAssessment(BaseModel):
    score: int = Field(ge=0, le=100)
    outcome: Outcome
    reasons: list[str]
    recommended_action: str
    score_breakdown: dict[str, float]


class ScreeningReport(BaseModel):
    document_type: str
    module_results: list[ModuleResult]
    contradictions: list[Contradiction]
    risk: RiskAssessment
