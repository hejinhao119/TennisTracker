from evidence.builder import build_evidence
from evidence.schemas import PoseObservation


def test_wrist_movement_keeps_frame_links() -> None:
    observations = [
        PoseObservation(10, 1, 0.9, tuple((0.0, 0.0) for _ in range(10)) + ((0.1, 0.2),)),
        PoseObservation(11, 1, 0.9, tuple((0.0, 0.0) for _ in range(10)) + ((0.2, 0.2),)),
    ]

    report = build_evidence("movement", [], observations)

    item = report.item("metric.pose.right_wrist_displacement")
    assert item.value == 0.1
    assert item.frame_refs == ((10, 11),)