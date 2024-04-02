import os
from ultralytics import YOLO

MODEL_PATH = "../models/obstacle_v2_320.pt"
IMAGES_PATH = "capture"

model = YOLO(MODEL_PATH)

if not os.path.exists('labels'):
    os.makedirs('labels')

image_files = [f for f in os.listdir(IMAGES_PATH) if f.endswith('.jpg') or f.endswith('.png')]
print(f"Found {len(image_files)} images in {IMAGES_PATH}")

results = model([os.path.join('capture', image_path) for image_path in image_files])

for i, r in enumerate(results):
    r.save_txt(os.path.join('labels', image_files[i].split('.')[0] + ".txt"))