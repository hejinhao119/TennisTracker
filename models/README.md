# `models/` Folder - README

## Overview

The `models/` directory contains the pre-trained YOLOv8 Pose models that are used for pose detection in this project. These models are specifically designed to detect human poses in tennis matches, allowing for advanced analytics such as stroke classification, player positioning, and movement tracking.

This folder contains only the model weight files for YOLOv8 pose estimation, which are loaded and utilized in the **pose estimator** module.

---

## Folder Structure

```plaintext
models/
├── yolov8n-pose.pt        # YOLOv8 Nano Pose Model (smaller, faster, lower accuracy)
├── yolov8x-pose-p6.pt     # YOLOv8 X-Pose Model (larger, more accurate)
