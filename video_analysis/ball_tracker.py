from pathlib import Path

import cv2

from evidence.schemas import BallObservation


def detect_ball(frame, frame_index: int) -> BallObservation:
    """Find a tennis-ball-colored candidate; return no detection when ambiguous."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = (20, 70, 80)
    upper = (90, 255, 255)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    height, width = frame.shape[:2]
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 8 or area > width * height * 0.01:
            continue
        (x, y), radius = cv2.minEnclosingCircle(contour)
        if radius < 2 or radius > min(width, height) * 0.04:
            continue
        circularity = area / (3.14159 * radius * radius)
        candidates.append((circularity, x, y, radius))
    if not candidates:
        return BallObservation(frame_index, None, None, 0.0)
    circularity, x, y, radius = max(candidates)
    confidence = min(1.0, max(0.0, circularity))
    return BallObservation(frame_index, x / width, y / height, confidence, radius / width)