# pose_estimation/test/test_yolo_pose_estimator.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from video_analysis.pose_estimator import detect_pose

def test_detect_pose():
    # Calculate the absolute path to the image
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    image_path = os.path.join(project_root, 'testing', 'tennis_match_image2.png')

    # Check if the image exists
    assert os.path.exists(image_path), f"Test image not found at {image_path}"

    # Run detection
    result = detect_pose(image_path)

    # Check if at least one person is detected
    assert len(result.keypoints.xy) > 0, "No person detected."

    print("test_detect_pose passed.")
