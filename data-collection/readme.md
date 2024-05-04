# Data Collection

## Initial Setup
Install necessary python packages into your environment. It's normal for this to take a while, especially when installing depthai.
```bash
pip install -r requirements.txt
```

## Capture
Simple utility to collect images and video from a connected OAK-D Camera. In the live view window, the below key presses correspond with their action. All images/videos are saved in the `capture/` directory. Make sure you're using a usb 3.0 cable.

| Key Press | Action |
| --- | --- |
| “q” | Quit the application |
| “c” | Capture a singular photo |
| “v” | Start/Stop taking a photo 5 times a second |
| “r” | Start/Stop recording a video |

```bash
python capture.py
```



## Annotate
Attempts to label every image in the `capture/` directory with the model specified by `MODEL_PATH` in the code. These image annotations are placed in the `labels/` folder and can be uploaded to roboflow along with the captured images. Using previous detection models to train new ones saves the time of manually annotating all collected images by hand.
```bash
python annotate.py
``` 