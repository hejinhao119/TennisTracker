from dataclasses import dataclass
from pathlib import Path

import cv2

from evidence.schemas import PoseObservation
from evidence.schemas import BallObservation

from .ball_tracker import detect_ball
from .pose_estimator import detect_pose_observation


@dataclass(frozen=True)
class VideoAnalysisResult:
    fps: float
    frame_count: int
    width: int
    height: int
    pose_observations: tuple[PoseObservation, ...]
    ball_observations: tuple[BallObservation, ...] = ()


def analyze_video(video_path: str | Path, sample_every: int = 30, max_samples: int = 120) -> VideoAnalysisResult:
    """Sample a video and return pose evidence; stroke classification remains separate."""
    if sample_every < 1 or max_samples < 1:
        raise ValueError("sample_every and max_samples must be positive")

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    fps = float(capture.get(cv2.CAP_PROP_FPS) or 0.0)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    observations: list[PoseObservation] = []
    ball_observations: list[BallObservation] = []
    frame_index = 0
    try:
        while len(observations) < max_samples:
            success, frame = capture.read()
            if not success:
                break
            if frame_index % sample_every == 0:
                observations.append(detect_pose_observation(frame, frame_index))
                ball_observations.append(detect_ball(frame, frame_index))
            frame_index += 1
    finally:
        capture.release()

    if not observations:
        raise ValueError("Video contained no readable frames")
    return VideoAnalysisResult(fps, frame_count, width, height, tuple(observations), tuple(ball_observations))