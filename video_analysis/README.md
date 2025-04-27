# Pose Estimation Module - README

## Overview

The **Pose Estimation** module is responsible for detecting and analysing human poses in tennis match videos using YOLOv8 models. The goal of this module is to provide detailed pose information, including keypoints of the body, such as the head, shoulders, elbows, wrists, hips, knees, and ankles, for each player.

## How It Works

1. **Input**: A video frame or image containing players in a tennis match.
2. **Detection**: The image is passed through a pre-trained YOLOv8 Pose model to detect the poses of the players.
3. **Pose Keypoints**: The model outputs a set of keypoints representing various body parts (head, shoulders, elbows, etc.).
4. **Annotation**: The keypoints are connected to form a skeleton, and the annotated image is generated.
5. **Output**: The annotated image or video frame is returned, showing the detected poses.

## Example Output
![Keypoint_Annotated_image](https://github.com/hejinhao119/TennisTracker/blob/main/testing/annotated_images/tennis_match_image1.jpg)