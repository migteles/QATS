import os
from datetime import datetime

def create_session_files():

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    os.makedirs("logs", exist_ok=True)
    os.makedirs("recordings", exist_ok=True)

    log_file = os.path.join("logs", f"session_{timestamp}.log")
    video_file = os.path.join("recordings", f"session_{timestamp}.mp4")

    return log_file, video_file
