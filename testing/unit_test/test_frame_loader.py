import sys
import os
import cv2
import numpy as np

# Add the TennisTracker root dir to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from video_analysis.frame_loader import load_video_frames

def test_extract_frames():
    video_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../tennis_match_video1.mp4'))
    
    frames = load_video_frames(video_path)

    # Check if frames are loaded correctly
    assert isinstance(frames, list)
    assert len(frames) > 0
    assert frames[0].shape[0] > 0 and frames[0].shape[1] > 0