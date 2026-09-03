import os
from dataclasses import dataclass


@dataclass(frozen=True)
class VisionSettings:
    model_path: str
    confidence_threshold: float = 0.35
    keypoint_threshold: float = 0.35
    image_size: int = 960
    device: str = "cpu"
    use_tracking: bool = True

    @classmethod
    def from_environment(cls) -> "VisionSettings":
        return cls(
            model_path=os.getenv("POSE_MODEL_PATH", "models/yolov8n-pose.pt"),
            confidence_threshold=float(os.getenv("POSE_CONFIDENCE_THRESHOLD", "0.35")),
            keypoint_threshold=float(os.getenv("POSE_KEYPOINT_THRESHOLD", "0.35")),
            image_size=int(os.getenv("POSE_IMAGE_SIZE", "960")),
            device=os.getenv("POSE_DEVICE", "cpu"),
            use_tracking=os.getenv("POSE_USE_TRACKING", "true").lower() in {"1", "true", "yes"},
        )

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence_threshold <= 1.0:
            raise ValueError("confidence threshold must be between 0 and 1")
        if not 0.0 <= self.keypoint_threshold <= 1.0:
            raise ValueError("keypoint threshold must be between 0 and 1")
        if self.image_size < 256:
            raise ValueError("image size must be at least 256")