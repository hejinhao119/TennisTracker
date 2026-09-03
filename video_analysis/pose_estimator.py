from ultralytics import YOLO
from pathlib import Path

from .settings import VisionSettings

# Load the YOLOv8 Pose model
settings = VisionSettings.from_environment()
model = YOLO(Path(settings.model_path).resolve() if Path(settings.model_path).is_absolute() else Path(__file__).resolve().parent.parent / settings.model_path)

def detect_pose(frame):
    """
    Detects pose on the given image frame.
    
    Args:
        frame (np.ndarray): Input image frame.

    Returns:
        annotated_frame (np.ndarray): Annotated image frame with pose landmarks.
    """
    results = model.predict(source=frame, save=False, conf=0.3)

    if results is None or len(results) == 0:
        return None

    annotated_frame = results[0].plot()
    return annotated_frame


def detect_pose_observation(frame, frame_index):
    """Return structured pose evidence without presenting it as stroke evidence."""
    from evidence.schemas import PoseObservation

    inference = model.track if settings.use_tracking else model.predict
    results = inference(
        source=frame,
        save=False,
        conf=settings.confidence_threshold,
        imgsz=settings.image_size,
        device=settings.device,
        persist=settings.use_tracking,
        verbose=False,
    )
    if not results:
        return PoseObservation(frame_index, 0, 0.0)

    result = results[0]
    person_count = len(result.boxes) if result.boxes is not None else 0
    if result.boxes is None or result.boxes.conf is None or person_count == 0:
        confidence = 0.0
        keypoint_confidence = 0.0
        keypoints = ()
        track_id = None
    else:
        box_confidences = result.boxes.conf
        primary_index = int(box_confidences.argmax().item())
        confidence = float(box_confidences[primary_index].item())
        height, width = frame.shape[:2]
        points = result.keypoints.xy[primary_index].tolist() if result.keypoints is not None else []
        keypoints = tuple((float(x) / width, float(y) / height) for x, y in points)
        point_confidences = result.keypoints.conf[primary_index] if result.keypoints is not None and result.keypoints.conf is not None else None
        keypoint_confidence = float(point_confidences.mean().item()) if point_confidences is not None else 0.0
        track_ids = result.boxes.id if result.boxes.id is not None else None
        track_id = int(track_ids[primary_index].item()) if track_ids is not None else None
    return PoseObservation(frame_index, person_count, confidence, keypoints, keypoint_confidence, track_id)
