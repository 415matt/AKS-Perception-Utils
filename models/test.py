import os
from ultralytics import YOLO

MODEL_PATH = "obstacle_v5_320.pt"
IMAGES_PATH = "capture"

model = YOLO(MODEL_PATH)

video_files = [os.path.join(IMAGES_PATH, f) for f in os.listdir(IMAGES_PATH) if f.endswith('.mp4') or f.endswith('.avi')]
print(f"Found {len(video_files)} images in {IMAGES_PATH}")


for v in video_files:
    r = model.predict(v, show_conf=True, save=True)