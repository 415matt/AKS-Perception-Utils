import cv2
import depthai as dai
import numpy as np
import time
import os
import time

def get_frame(queue):
    # Get frame from queue and convert to OpenCV format
    return queue.get().getCvFrame()

def get_color_camera(pipeline):
    # Configure color camera
    color = pipeline.createColorCamera()
    color.setResolution(dai.ColorCameraProperties.SensorResolution.THE_720_P)
    color.setVideoSize(1280, 720)
    
    # Set initial controls for sharpness and denoise
    color.initialControl.setSharpness(2)     # Adjusted to a mid-range value
    color.initialControl.setLumaDenoise(1)   # Default value
    color.initialControl.setChromaDenoise(1) # Default value
    
    # Set the camera to use the default board socket
    color.setBoardSocket(dai.CameraBoardSocket.AUTO)
    
    return color

def set_window_size(window_name, width, height):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, width, height)

def create_capture_folder(folder_name):
    # Create capture folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def get_max_image_index(folder_name):
    # Get the maximum image index from the capture folder
    existing_images = [int(file.split('.')[0]) for file in os.listdir(folder_name) if (file.endswith('.jpg') or file.endswith('.mp4'))]
    return max(existing_images) if existing_images else 0

if __name__ == '__main__':
    # Define a pipeline
    dai_pipeline = dai.Pipeline()
    
    # Set up main camera
    color_main = get_color_camera(dai_pipeline)
    
    # Set output Xlink for main camera
    xout_main = dai_pipeline.createXLinkOut()
    xout_main.setStreamName("video")
    color_main.video.link(xout_main.input)
    
    # Create and set up the capture folder
    capture_folder = "capture"
    create_capture_folder(capture_folder)
    
    # Determine the starting capture counter
    capture_counter = get_max_image_index(capture_folder) + 1
    
    # Define capturing parameters
    capturing = False
    capture_interval = 1 / 5  # 5 fps
    last_capture_time = time.time()

    # Define video recording parameters
    video_writer = None
    video_recording = False
    video_file_name = None
    video_fps = 20  # Set the frames per second for the video
    video_codec = cv2.VideoWriter_fourcc(*'mp4v')
    
    # Start the device with the pipeline
    with dai.Device(dai_pipeline) as device:
        set_window_size("video", 640, 400)
        video_queue = device.getOutputQueue(name="video", maxSize=1)
        
        while True:
            raw_frame = get_frame(video_queue)
            
            # Display output image
            cv2.imshow("video", raw_frame)
            
            # Check for keyboard input
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('c'):
                frame_name = os.path.join(capture_folder, f"{capture_counter}.jpg")
                cv2.imwrite(frame_name, raw_frame)
                print(f"Image {capture_counter} captured and saved.")
                capture_counter += 1
            elif key == ord('v'):
                capturing = not capturing
                print("Capturing at 5 fps." if capturing else "Stopped capturing.")
            elif key == ord('r'):
                if video_recording:
                    # Stop video recording
                    video_recording = False
                    video_writer.release()
                    video_writer = None
                    print(f"Stopped recording. Video saved as {video_file_name}")
                    capture_counter += 1
                    time.sleep(1)
                else:
                    # Start video recording
                    video_recording = True
                    video_file_name = os.path.join(capture_folder, f"{capture_counter}.mp4")
                    video_writer = cv2.VideoWriter(video_file_name, video_codec, video_fps, (1280, 720))
                    print(f"Started recording video {capture_counter}.mp4")
            
            # Capture frames at 5 fps
            if capturing and (time.time() - last_capture_time) >= capture_interval:
                frame_name = os.path.join(capture_folder, f"{capture_counter}.jpg")
                cv2.imwrite(frame_name, raw_frame)
                print(f"Image {capture_counter} captured at 5 fps.")
                capture_counter += 1
                last_capture_time = time.time()

            if video_recording:
                video_writer.write(raw_frame)


        
        # Release the OpenCV window and clean up resources
        if video_writer is not None and video_recording:
            video_writer.release()
        cv2.destroyAllWindows()