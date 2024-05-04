# AKS Perception Utils
This repository contains a variety of utilities for perception-related tasks as part of UCSD's participation in the [Autonomous Karting Series](https://www.autonomouskartingseries.com/).

## Utilities:

### Data Collection
- Capture photos individually or in bursts at a rate of 5 photos per second using OAKD Cameras. This is useful for collecting training and test data.
- Utilize pre-trained models to automatically generate annotations on unseen data. This can save time compared to manual annotation.

### ROS Bag Reader
- Convert ROS bag (.mcap) files into a series of images and optionally create a video file. Useful for pulling images directly from ROS.

### Models
- Evaluate the performance of the model by running inference on videos located in the `data-collection/capture` directory.
- Downloadable weights for AKS obstacle detection models.

### Training
- Template notebook to train YOLOv8 models in other environments such as Google Collab.