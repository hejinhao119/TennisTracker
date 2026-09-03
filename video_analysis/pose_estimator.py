from ultralytics import YOLO
from pathlib import Path

# Load the YOLOv8 Pose model
model = YOLO(Path(__file__).resolve().parent.parent / 'models' / 'yolov8n-pose.pt')

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

    results = model.predict(source=frame, save=False, conf=0.3, verbose=False)
    if not results:
        return PoseObservation(frame_index, 0, 0.0)

    result = results[0]
    person_count = len(result.boxes) if result.boxes is not None else 0
    if result.boxes is None or result.boxes.conf is None or person_count == 0:
        confidence = 0.0
        keypoints = ()
    else:
        box_confidences = result.boxes.conf
        primary_index = int(box_confidences.argmax().item())
        confidence = float(box_confidences[primary_index].item())
        height, width = frame.shape[:2]
        points = result.keypoints.xy[primary_index].tolist() if result.keypoints is not None else []
        keypoints = tuple((float(x) / width, float(y) / height) for x, y in points)
    return PoseObservation(frame_index, person_count, confidence, keypoints)
