from dataclasses import dataclass, field
from typing import Literal

Severity = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class AgentFinding:
    finding_id: str
    category: str
    severity: Severity
    claim: str
    confidence: float
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("agent confidence must be between 0 and 1")
        if not self.evidence_refs:
            raise ValueError("every finding must cite evidence")


@dataclass(frozen=True)
class AgentReport:
    agent_name: str
    summary: str
    findings: tuple[AgentFinding, ...] = ()
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True)
class CoachRecommendation:
    priority: int
    issue: str
    rationale: str
    drill: str
    frequency: str
    volume: str
    confidence: float
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class CoachReport:
    diagnosis: str
    recommendations: tuple[CoachRecommendation, ...]
    agreements: tuple[str, ...] = ()
    contradictions: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()


@dataclass(frozen=True)
class CriticReport:
    approved: bool
    issues: tuple[str, ...] = ()


@dataclass(frozen=True)
class CoachingRun:
    match: AgentReport
    biomechanics: AgentReport
    tactical: AgentReport
    coach: CoachReport
    critic: CriticReport
    attempts: int