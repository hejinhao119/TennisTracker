from evidence.builder import build_evidence
from evidence.schemas import PoseObservation


def test_pose_coverage_is_traceable_without_stroke_claims() -> None:
    report = build_evidence(
        "session-1",
        [],
        [PoseObservation(0, 1, 0.9), PoseObservation(30, 0, 0.0)],
    )

    item = report.item("metric.pose.detection_rate")
    assert item.value == 0.5
    assert item.frame_refs == ((0, 0),)
    assert report.strokes == ()