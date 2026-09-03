import pytest

from video_analysis.settings import VisionSettings


def test_vision_settings_are_configurable(monkeypatch) -> None:
    monkeypatch.setenv("POSE_IMAGE_SIZE", "1280")
    monkeypatch.setenv("POSE_DEVICE", "cpu")
    monkeypatch.setenv("POSE_USE_TRACKING", "false")

    settings = VisionSettings.from_environment()

    assert settings.image_size == 1280
    assert settings.device == "cpu"
    assert settings.use_tracking is False


def test_vision_settings_reject_invalid_threshold() -> None:
    with pytest.raises(ValueError):
        VisionSettings("models/yolov8n-pose.pt", confidence_threshold=1.1)