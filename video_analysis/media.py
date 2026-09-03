from pathlib import Path
from tempfile import NamedTemporaryFile

import cv2

from evidence.schemas import PoseObservation


def movement_series(observations: tuple[PoseObservation, ...]) -> list[dict[str, float]]:
    """Build chart-ready movement rows from consecutive pose observations."""
    rows: list[dict[str, float]] = []
    for previous, current in zip(observations, observations[1:]):
        if len(previous.keypoints) <= 10 or len(current.keypoints) <= 10:
            continue
        previous_wrist = previous.keypoints[10]
        current_wrist = current.keypoints[10]
        displacement = ((current_wrist[0] - previous_wrist[0]) ** 2 + (current_wrist[1] - previous_wrist[1]) ** 2) ** 0.5
        rows.append({
            "frame": float(current.frame_index),
            "wrist_displacement": displacement,
            "pose_confidence": current.confidence,
        })
    return rows


def extract_frame(video_path: str | Path, frame_index: int):
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    try:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        success, frame = capture.read()
        if not success:
            raise ValueError(f"Could not read frame {frame_index}")
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    finally:
        capture.release()


def create_clip(video_path: str | Path, frame_start: int, frame_end: int, fps: float) -> bytes:
    """Create a short MP4 around an evidence reference for Streamlit playback."""
    if frame_start < 0 or frame_end < frame_start or fps <= 0:
        raise ValueError("invalid clip bounds")
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise ValueError(f"Could not open video: {video_path}")
    try:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_start)
        success, first_frame = capture.read()
        if not success:
            raise ValueError("Could not read clip start")
        height, width = first_frame.shape[:2]
        with NamedTemporaryFile(suffix=".mp4", delete=False) as clip_file:
            clip_path = clip_file.name
        writer = cv2.VideoWriter(
            clip_path,
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height),
        )
        try:
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_start)
            for _ in range(frame_end - frame_start + 1):
                success, frame = capture.read()
                if not success:
                    break
                writer.write(frame)
        finally:
            writer.release()
        return Path(clip_path).read_bytes()
    finally:
        capture.release()