import cv2

def load_video_frames(video_path, skip=1):
    """Loads frames from video and returns them as a list."""
    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_idx = 0

    # Check if the video opened successfully
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % skip == 0:
            frames.append(frame)
        frame_idx += 1
    cap.release()

    # Return the list of frames
    return frames