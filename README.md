# Hand Gesture Controlled Volume

## Description

This project enables users to control their computer's volume level through hand gestures. It leverages computer vision and machine learning technologies to recognize hand gestures with a webcam and adjusts the system's volume accordingly. The project is comprised of two main scripts:

- `handcontrol.py`: A module for detecting hand gestures using OpenCV and MediaPipe, offering a comprehensive hand tracking interface.
- `volume.py`: An application that employs the `handcontrol.py` module to modify the system's volume based on the distance between the thumb and index finger.

## Installation

Ensure you have Python 3.6 or later installed on your system. You will also need to install several packages, which can be done via pip. Open your terminal or command prompt and execute the following command:

```sh
pip install opencv-python mediapipe numpy comtypes pycaw
```


## Usage
To use this application, follow these steps:

Ensure your webcam is connected and properly set up.
Run the volume.py script by navigating to the project directory and executing:
```sh
python volume.py
```

Adjust the volume by moving your thumb and index finger closer together or further apart. The volume increases as the distance between these two fingers increases and decreases as the distance shortens.

## Code in Action

https://github.com/sushanmali50/volume-cntrl-cv2/assets/145068266/d712af21-4fb9-4f51-8177-f17b0973ff2f

