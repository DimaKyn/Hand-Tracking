import HandTrackingModule as htm
import mediapipe as mp
import cv2
import time

cap = cv2.VideoCapture(0)
tracker = htm.handTracker()

# Write fps
prevTime = 0
currTime = 0

while True:
        success, image = cap.read()
        image = tracker.handsFinder(image)
        lmList = tracker.positionFinder(image)
        if len(lmList) != 0:
            print(lmList[4])

        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime

        # Put fps counter on the screen
        cv2.putText(image, str(int(fps)), (0, 25), cv2.FONT_HERSHEY_PLAIN, 2,
                    (200, 100, 200), 3)

        cv2.imshow("Video", image)
        cv2.waitKey(1)