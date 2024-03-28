import cv2
import time
import numpy as np
import handcontrol as htm  # Import the previously defined hand tracking module
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # Library for controlling system volume

# Camera settings
wCam, hCam = 640, 480

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0  # To calculate frames per second

# Initialize the hand detector with a custom detection confidence
detector = htm.handDetector(detectionCon=0.6)

# Get the default audio device using the pycaw library
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Get the volume range of the system
volRange = volume.GetVolumeRange()

minVol = volRange[0]  # Minimum volume
maxVol = volRange[1]  # Maximum volume
volBar = 400  # Initial volume bar height
vol = 0  # Initial volume level

while True:
    success, img = cap.read()
    img = detector.findHands(img)  # Detect hands
    lmList = detector.findPosition(img, draw=False)  # Get landmark positions

    if len(lmList) != 0:
        # Get the positions of the thumb tip and index finger tip
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        # Calculate the center point between the two fingertips
        cx, cy = (x1+x2) // 2, (y1+y2) // 2

        # Draw circles at the fingertips and a line between them
        cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.circle(img, (cx, cy), 11, (255, 0, 0), cv2.FILLED)

        # Calculate the distance between the thumb and index finger tips
        length = math.hypot(x2-x1, y2-y1)

        # Interpolate the length to a volume level
        vol = np.interp(length, [20, 200], [minVol, maxVol])
        # Interpolate the length to a position of the volume bar
        volBar = np.interp(length, [20, 200], [400, 150])
        # Set the system volume
        volume.SetMasterVolumeLevel(vol, None)

        # If the distance is very small, indicate this with a green circle
        if length < 25:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    # Draw a rectangle for the volume bar and fill it based on the current volume
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

    # Calculate and display the FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 0, 255), 3)

    # Display the image
    cv2.imshow("Img", img)
    cv2.waitKey(1)
