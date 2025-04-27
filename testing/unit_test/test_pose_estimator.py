import sys
import os
import cv2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from video_analysis.pose_estimator import detect_pose

def test_detect_pose():
    # Calculate the absolute path to the image
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    image_path = os.path.join(project_root, 'testing', 'tennis_match_image2.png')

    # Check if the image exists
    assert os.path.exists(image_path), f"Test image not found at {image_path}"

    # Load the image
    frame = cv2.imread(image_path)
    assert frame is not None, f"Failed to load image from {image_path}"

    # Run detection
    annotated_frame = detect_pose(frame)

    # Check if detection is successful
    assert annotated_frame is not None, "Pose detection failed, annotated frame is None."

    # Save the annotated image
    save_dir = os.path.join(project_root, 'testing', 'annotated_images')
    os.makedirs(save_dir, exist_ok=True)  # Make sure the folder exists
    save_path = os.path.join(save_dir, 'tennis_match_image2.png')
    cv2.imwrite(save_path, annotated_frame)

    # Check if the annotated image was saved successfully
    assert os.path.exists(save_path), f"Annotated image not saved at {save_path}"

    print(f"test_detect_pose passed. Annotated image saved to {save_path}")
