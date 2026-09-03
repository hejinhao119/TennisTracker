import cv2
import numpy as np

from evidence.builder import build_evidence
from video_analysis.ball_tracker import detect_ball


def test_ball_tracker_detects_colored_candidate_and_trajectory() -> None:
    first = np.zeros((180, 320, 3), dtype=np.uint8)
    second = first.copy()
    cv2.circle(first, (100, 90), 6, (0, 220, 180), -1)
    cv2.circle(second, (130, 90), 6, (0, 220, 180), -1)
    observations = [detect_ball(first, 10), detect_ball(second, 20)]

    report = build_evidence("ball", [], ball_observations=observations)

    assert report.item("metric.ball.detection_rate").value == 1.0
    assert report.item("metric.ball.normalized_displacement").value > 0.05