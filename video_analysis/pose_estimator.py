from ultralytics import YOLO
import cv2

# Load the YOLOv8 Pose model
model = YOLO('../models/yolov8n-pose.pt')

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
