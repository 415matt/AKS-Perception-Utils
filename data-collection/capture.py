import cv2
import depthai as dai
import numpy as np
import time
import os

def get_frame(queue):
    # Get frame from queue
    frame = queue.get()
    # Convert frame to OpenCV format and return
    return frame.getCvFrame()

def get_color_camera(pipeline):
    # Configure color camera
    color = pipeline.createColorCamera()
    
    # Set Camera Resolution
    color.setResolution(dai.ColorCameraProperties.SensorResolution.THE_720_P)
    color.setVideoSize(1280, 720)
    
    # Make video sharper?
    color.initialControl.setSharpness(4)     # range: 0..4, default: 1
    color.initialControl.setLumaDenoise(0)   # range: 0..4, default: 1
    color.initialControl.setChromaDenoise(0) # range: 0..4, default: 1
    
    # Get main camera
    color.setBoardSocket(dai.CameraBoardSocket.AUTO)
    
    return color

def set_window_size(width, height):
    cv2.namedWindow("video", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("video", width, height)

if __name__ == '__main__':
    
    # Define a pipeline
    dai_pipeline = dai.Pipeline()
    
    # Set up main camera
    color_main = get_color_camera(dai_pipeline)
    
    # Set output Xlink for main camera
    xout_main = dai_pipeline.createXLinkOut()
    xout_main.setStreamName("video")
  
    # Attach cameras to output Xlink
    color_main.video.link(xout_main.input)
    
    with dai.Device(dai_pipeline) as device:
        
        set_window_size(640, 400)
        
        # Get output queues. 
        video_queue = device.getOutputQueue(name="video", maxSize=1)

        # Set display window name
        cv2.namedWindow("video")

        # Variable used to toggle between three views
        view_counter = 0
        
        # Initiate capture counter
        existing_images = [int(file.split('.')[0]) for file in os.listdir("capture") if file.endswith('.jpg')]
        if existing_images:
            capture_counter = max(existing_images) + 1
        else:
            capture_counter = 1

        # Capturing state and timer
        capturing = False
        capture_interval = 1 / 5  # Capture every 1/5 seconds to achieve 5 fps
        last_capture_time = time.time()
        
        while True:
            # Get raw frame
            raw_frame = get_frame(video_queue)
            im_out = raw_frame
            
            # Display output image
            cv2.imshow("video", im_out)
            
            # Check for keyboard input
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('t'):
                view_counter = (view_counter + 1) % 2
            elif key == ord('c'):
                frame_name = os.path.join("capture", f"{capture_counter}.jpg")
                cv2.imwrite(frame_name, im_out)
                print(f"Image {capture_counter} captured and saved.")
                capture_counter += 1
            elif key == ord('v'):
                # Toggle capturing state when 'v' is pressed
                capturing = not capturing
                if capturing:
                    print("Started capturing at 5 fps.")
                else:
                    print("Stopped capturing.")
            
            # Capture frames at 5 fps
            if capturing and (time.time() - last_capture_time) >= capture_interval:
                frame_name = os.path.join("capture", f"{capture_counter}.jpg")
                cv2.imwrite(frame_name, im_out)
                print(f"Image {capture_counter} captured at 5 fps.")
                capture_counter += 1
                last_capture_time = time.time()
        
        # Release the OpenCV window and clean up resources
        cv2.destroyAllWindows()