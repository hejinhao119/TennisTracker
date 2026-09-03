from evidence.schemas import PoseObservation
from video_analysis.media import movement_series


def test_movement_series_is_chart_ready() -> None:
    point = tuple((0.0, 0.0) for _ in range(10))
    observations = (
        PoseObservation(10, 1, 0.9, point + ((0.1, 0.2),)),
        PoseObservation(20, 1, 0.8, point + ((0.3, 0.2),)),
    )

    rows = movement_series(observations)

    assert rows[0]["frame"] == 20.0
    assert abs(rows[0]["wrist_displacement"] - 0.2) < 1e-9
    assert rows[0]["pose_confidence"] == 0.8