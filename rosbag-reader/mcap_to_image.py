from concurrent.futures import ThreadPoolExecutor, as_completed
from mcap_ros2.reader import read_ros2_messages
import numpy as np
import cv2
import os
from tqdm import tqdm
import datetime

TOPIC_NAME = "/oak/rgb/image_raw"
MCAP_DIR = "mcap_file"
OUTPUT_DIR = "output"
VIDEO_FRAME_RATE = 30

def read_binary_image(binary_data, width, height, encoding='bgr8'):
    if encoding != 'bgr8':
        raise ValueError(f"Unsupported encoding: {encoding}")
    image_data = np.frombuffer(binary_data, dtype=np.uint8).reshape((height, width, 3))
    return image_data

def save_image(binary_data, width, height, encoding, image_counter):
    image_data = read_binary_image(binary_data, width, height, encoding)
    filepath = os.path.join(OUTPUT_DIR, f'{image_counter}.jpg')
    cv2.imwrite(filepath, image_data)

if __name__ == '__main__':
    mcap_files = [os.path.join(MCAP_DIR, f) for f in os.listdir(MCAP_DIR) if f.endswith('.mcap')]

    for i,f in enumerate(mcap_files):
        save_video = "y" in input(f"Do you also want to save {f} to video? (y/n): ").lower()

        print("Loading messages into memory...")
        messages = [(msg.ros_msg.data, msg.ros_msg.width, msg.ros_msg.height, msg.ros_msg.encoding, i) for i, msg in enumerate(read_ros2_messages(f, topics=[TOPIC_NAME]))]

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            future_to_index = {executor.submit(save_image, *message): message[-1] for message in messages}

            for future in tqdm(as_completed(future_to_index), total=len(messages), desc="Processing Images"):
                image_counter = future_to_index[future]
        print("Done!")
    
        if save_video:
            output_dir, frame_rate = OUTPUT_DIR, VIDEO_FRAME_RATE
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            video_writer = cv2.VideoWriter(f"{os.path.join(OUTPUT_DIR, f'output_{timestamp}.avi')}", cv2.VideoWriter_fourcc(*'XVID'), frame_rate, cv2.imread(os.path.join(output_dir, sorted(os.listdir(output_dir))[-1])).shape[1::-1])
            image_files = sorted(filter(lambda x: x.endswith(".jpg"), os.listdir(output_dir)), key=lambda x: int(x.split('.')[0]))
            for image in tqdm(image_files, desc="Writing images to video"):
                video_writer.write(cv2.imread(os.path.join(output_dir, image)))

            video_writer.release()
            print("Done!")