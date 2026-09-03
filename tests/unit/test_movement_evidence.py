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


def test_movement_profile_exposes_activity_and_variability() -> None:
    point = tuple((0.0, 0.0) for _ in range(10))
    observations = tuple(
        PoseObservation(frame, 1, 0.9, point + ((position, 0.2),))
        for frame, position in ((0, 0.1), (1, 0.2), (2, 0.8), (3, 0.9), (4, 1.0), (5, 1.0), (6, 1.0), (7, 1.0), (8, 1.0))
    )

    report = build_evidence("profile", [], list(observations))

    assert report.item("metric.pose.wrist_movement.active_ratio").value > 0
    assert report.item("metric.pose.wrist_movement.variability").value > 0