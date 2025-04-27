# pose_estimation/yolo_pose_estimator.py

from ultralytics import YOLO
import cv2

# Load the YOLOv8 Pose model
model = YOLO('../models/yolov8n-pose.pt')

def detect_pose(image_path):
    """
    Detect human poses in an image.

    Args:
        image_path (str): Path to the input image.

    Returns:
        result (Results object): The result containing keypoints and other information.
    """
    # Read image
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Image at {image_path} cannot be loaded.")

    # Run inference
    results = model.predict(source=img, save=False, imgsz=640, conf=0.3)

    return results[0]
