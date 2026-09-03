from evidence.builder import build_evidence
from evidence.schemas import StrokeObservation


def test_evidence_aggregates_metrics_and_preserves_frames() -> None:
    strokes = [
        StrokeObservation("s1", 1.0, "forehand", 0.9, 10, 12, contact_point_x=0.4),
        StrokeObservation("s2", 2.0, "forehand", 0.8, 20, 22, contact_point_x=0.6),
        StrokeObservation("s3", 3.0, "backhand", 0.7, 30, 32),
    ]

    report = build_evidence("session-1", strokes)

    assert report.item("metric.stroke_share.forehand").value == 2 / 3
    assert report.item("metric.contact_point.behind_target_ratio").value == 0.5
    assert report.item("metric.contact_point.behind_target_ratio").frame_refs == ((10, 12),)


def test_empty_evidence_is_explicit() -> None:
    report = build_evidence("session-empty", [])

    assert report.items == ()
    assert "No valid strokes were detected" in report.missing_data


def test_invalid_confidence_is_rejected() -> None:
    try:
        StrokeObservation("s1", 1.0, "forehand", 1.1, 1, 2)
    except ValueError as error:
        assert "confidence" in str(error)
    else:
        raise AssertionError("invalid confidence was accepted")