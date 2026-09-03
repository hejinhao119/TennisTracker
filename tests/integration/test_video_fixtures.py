from pathlib import Path

import cv2
import numpy as np

from video_analysis.media import create_clip
from video_analysis.session_analyzer import analyze_video


def _write_synthetic_video(path: Path, frame_count: int, shift: int) -> None:
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*"mp4v"), 10.0, (320, 180))
    try:
        for frame_index in range(frame_count):
            frame = np.zeros((180, 320, 3), dtype=np.uint8)
            center = (80 + frame_index * shift, 90)
            cv2.circle(frame, center, 24, (0, 180, 0), -1)
            writer.write(frame)
    finally:
        writer.release()


def test_analyzer_and_clip_support_a_second_fixture(tmp_path: Path, monkeypatch) -> None:
    video_path = tmp_path / "synthetic_session_b.mp4"
    _write_synthetic_video(video_path, frame_count=12, shift=3)

    monkeypatch.setattr(
        "video_analysis.session_analyzer.detect_pose_observation",
        lambda frame, frame_index: __import__("evidence").PoseObservation(frame_index, 1, 0.8),
    )
    result = analyze_video(video_path, sample_every=2, max_samples=6)
    clip = create_clip(video_path, 2, 6, result.fps)

    assert len(result.pose_observations) == 6
    assert result.width == 320 and result.height == 180
    assert clip.startswith(b"\x00\x00\x00")