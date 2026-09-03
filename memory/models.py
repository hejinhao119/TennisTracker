from dataclasses import dataclass


@dataclass(frozen=True)
class SessionMetric:
    session_id: str
    metric: str
    value: float
    sample_count: int
    confidence: float


@dataclass(frozen=True)
class MetricComparison:
    metric: str
    previous_value: float
    current_value: float
    change: float
    meaningful: bool
    reason: str
