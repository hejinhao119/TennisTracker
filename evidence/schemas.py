from dataclasses import dataclass, field
from typing import Any, Literal

Reliability = Literal["low", "medium", "high"]


def _bounded_confidence(value: float, name: str) -> float:
    value = float(value)
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


@dataclass(frozen=True)
class StrokeObservation:
    """Raw, structured output from a vision pipeline for one stroke."""

    stroke_id: str
    timestamp: float
    stroke_type: str
    confidence: float
    frame_start: int
    frame_end: int
    contact_point_x: float | None = None
    pose_metrics: dict[str, float] = field(default_factory=dict)
    movement_metrics: dict[str, float] = field(default_factory=dict)
    outcome: str | None = None

    def __post_init__(self) -> None:
        if not self.stroke_id or self.frame_start < 0 or self.frame_end < self.frame_start:
            raise ValueError("stroke identity and frame range are invalid")
        if self.timestamp < 0:
            raise ValueError("timestamp cannot be negative")
        _bounded_confidence(self.confidence, "confidence")
        if self.contact_point_x is not None and not 0.0 <= self.contact_point_x <= 1.0:
            raise ValueError("contact_point_x must be normalized between 0 and 1")


@dataclass(frozen=True)
class PoseObservation:
    """A frame-level pose detection that has not been classified as a stroke."""

    frame_index: int
    person_count: int
    confidence: float

    def __post_init__(self) -> None:
        if self.frame_index < 0 or self.person_count < 0:
            raise ValueError("pose frame index and person count are invalid")
        _bounded_confidence(self.confidence, "pose confidence")


@dataclass(frozen=True)
class EvidenceItem:
    """An auditable metric available to agents, with provenance and uncertainty."""

    evidence_id: str
    metric: str
    value: Any
    unit: str
    source: str
    measurement_confidence: float
    sample_count: int
    reliability: Reliability
    frame_refs: tuple[tuple[int, int], ...] = ()

    def __post_init__(self) -> None:
        if not self.evidence_id or not self.metric or self.sample_count < 0:
            raise ValueError("evidence identity and sample count are invalid")
        _bounded_confidence(self.measurement_confidence, "measurement_confidence")


@dataclass(frozen=True)
class EvidenceReport:
    session_id: str
    strokes: tuple[StrokeObservation, ...]
    items: tuple[EvidenceItem, ...]
    pose_observations: tuple[PoseObservation, ...] = ()
    missing_data: tuple[str, ...] = ()
    suspicious_data: tuple[str, ...] = ()

    def item(self, evidence_id: str) -> EvidenceItem:
        for item in self.items:
            if item.evidence_id == evidence_id:
                return item
        raise KeyError(evidence_id)