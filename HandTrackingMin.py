import cv2
import mediapipe as mp
import time

# Uses the i webcam
cap = cv2.VideoCapture(0)

# Mediapipe hands
mpHands = mp.solutions.hands

# hands is a Hands object
# Hands(Keep tracking when no hand is found[T/F],maxNumOfHands INT,...
# ...,minimum detection confidence FLOAT, minimum tracking confidence FLOAT)
hands = mpHands.Hands(False)

# Method for drawing lines between every dot on the hand
mpDraw = mp.solutions.drawing_utils

# Write fps
prevTime = 0
currTime = 0

while True:
    success, img = cap.read()

    # Image object
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # "process" is a method which processes the image of the camera
    results = hands.process(imgRGB)

    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handsLms in results.multi_hand_landmarks:
            # id = index of finger landmark
            # Print landmark locations by pixels on the screen
            for id, landmark in enumerate(handsLms.landmark):
                print(id, landmark)
                height, width, channel = img.shape
                # Position of center of the image
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                print(id, cx, cy)

                if id == 0:
                    cv2.circle(img, (cx, cy), 20, (255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handsLms, mpHands.HAND_CONNECTIONS)

    currTime = time.time()
    fps = 1 / (currTime-prevTime)
    prevTime = currTime

    # Put fps counter on the screen
    cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                (200, 100, 200), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
