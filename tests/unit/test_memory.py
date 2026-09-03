from evidence.builder import build_evidence
from evidence.schemas import StrokeObservation
from memory.repository import SessionRepository
from memory.session_history import compare_metric
from memory.models import SessionMetric


def test_session_metrics_round_trip_and_history(tmp_path) -> None:
    repository = SessionRepository(tmp_path / "sessions.db")
    report = build_evidence(
        "session-1",
        [StrokeObservation(str(i), float(i), "forehand", 0.8, i, i + 1) for i in range(8)],
    )

    repository.save_evidence(report)
    history = repository.get_metric_history("metric.stroke_share.forehand")

    assert len(history) == 1
    assert history[0].value == 1.0
    assert history[0].sample_count == 8


def test_comparison_declines_to_overclaim_small_samples() -> None:
    previous = SessionMetric("old", "contact", 0.7, 4, 0.9)
    current = SessionMetric("new", "contact", 0.4, 20, 0.9)

    comparison = compare_metric(previous, current)

    assert abs(comparison.change - (-0.3)) < 1e-9
    assert not comparison.meaningful
    assert "Insufficient" in comparison.reason