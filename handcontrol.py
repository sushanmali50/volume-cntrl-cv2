import cv2
import mediapipe as mp
import time

class handDetector():
    # Initialize the hand detector class with optional parameters for the hand tracking model.
    def __init__(self, mode=False, maxHands=2, modelComp=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode  # Whether to treat the input images as a batch or single image.
        self.maxHands = maxHands  # Maximum number of hands to detect.
        self.detectionCon = detectionCon  # Minimum detection confidence threshold.
        self.trackCon = trackCon  # Minimum tracking confidence threshold.
        self.modelComp = modelComp  # Model complexity: 0, 1, or 2.

        # Initialize MediaPipe Hands.
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.modelComp, self.detectionCon, self.trackCon)
        # Initialize MediaPipe Drawing utility.
        self.mpDraw = mp.solutions.drawing_utils

    # Method to find hands in an image.
    def findHands(self, img, draw=True):
        # Convert image from BGR to RGB.
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process the image to find hands.
        self.results = self.hands.process(imgRGB)

        # If hands are detected, draw them.
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    # Method to find the position of hand landmarks.
    def findPosition(self, img, handNo=0, draw=True):
        lmList = []  # List to store landmark positions.
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # Calculate the position of each landmark.
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # Append landmark ID and position to the list.
                lmList.append([id, cx, cy])
                if draw:
                    # Draw a circle for each landmark.
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList

# Main function to execute the hand detection.
def main():
    pTime = 0  # Previous time for calculating FPS.
    cTime = 0  # Current time for calculating FPS.
    cap = cv2.VideoCapture(0)  # Start video capture.
    detector = handDetector()  # Create a hand detector object.
    
    while True:
        success, img = cap.read()  # Read frames from the video capture.
        img = detector.findHands(img)  # Detect hands in the image.
        lmList = detector.findPosition(img)  # Get landmark positions.

        if len(lmList) != 0:
            print(lmList[4])  # Print the position of the fifth landmark.

        # Calculate and display FPS.
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        # Show the image in a window.
        cv2.imshow("Image", img)
        cv2.waitKey(1)  # Wait for a key press to exit.

if __name__ == "__main__":
    main()
