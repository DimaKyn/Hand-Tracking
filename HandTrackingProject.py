import time
import HandTrackingModule as htm
import mediapipe as mp
import cv2
import pyautogui
import webbrowser
import numpy as np
import spotify


# Creates a delay of x seconds between each action
def delay30(x):
    time_now = time.time()
    time_delay = time.time() + x
    while True:
        if time_now >= time_delay:
            break
        time_now = time.time()
    #####################################################


def checkIfTouching(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5):
    return (abs(x1 - x2) + abs(y1 - y2) < 30)   \
           & (abs(x1 - x3) + abs(y1 - y3) > 60) \
           & (abs(x1 - x4) + abs(y1 - y4) > 60) \
           & (abs(x1 - x5) + abs(y1 - y5) > 60)


# url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
# webbrowser.register('chrome',
#                     None, webbrowser.BackgroundBrowser(
#         "C:\Program Files\Google\Chrome\Application//chrome.exe"))

# Uses the i webcam
cap = cv2.VideoCapture(0)

# tracker is a hand tracker class
tracker = htm.handTracker()

# Write fps
prevTime = 0
currTime = 0

pyautogui.press('play-pause')
# Display image, find hands, then find their position
while True:
    success, image = cap.read()
    image = tracker.handsFinder(image)
    lmList, xlmList, ylmList = tracker.positionFinder(image)
    if len(lmList) != 0:

        # Thumb
        x1, y1 = xlmList[4], ylmList[4]
        # Index finger coordinates
        x2, y2 = xlmList[8], ylmList[8]
        # Middle finger coordinates
        x3, y3 = xlmList[12], ylmList[12]
        # Ring finger coordinates
        x4, y4 = xlmList[16], ylmList[16]
        # Pinky finger
        x5, y5 = xlmList[20], ylmList[20]

        # # Toggle Hand Control (Thumb and pinky finger touching)
        # if (checkIfTouching(x1,y1,x5,y5,x2,y2,x3,y3,x4,y4)):
        #     pyautogui.hold("alt", "tab")
        #     print("HAND CONTROL - ON")
        #     delay30(0.7)
        #     while True:
        #         lmList, xlmList, ylmList = tracker.positionFinder(image)
                # Thumb
                # x1, y1 = xlmList[4], ylmList[4]
                # # Index finger coordinates
                # x2, y2 = xlmList[8], ylmList[8]
                # # Middle finger coordinates
                # x3, y3 = xlmList[12], ylmList[12]
                # # Ring finger coordinates
                # x4, y4 = xlmList[16], ylmList[16]
                # # Little finger
                # x5, y5 = xlmList[20], ylmList[20]
                # Play music (Insures middle finger is close to ring finger) 👌
        if checkIfTouching(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5):
                    pyautogui.press('playpause')
                    print("PLAY")
                    # Create a 0.7-second delay
                    delay30(0.5)

                # Next Track (Middle finger and thumb touching)
        if checkIfTouching(x1, y1, x3, y3, x2, y2, x4, y4, x5, y5):
                    pyautogui.press('nexttrack')
                    print("Previous Track")
                    # Create a 0.7-second delay
                    delay30(0.5)

                # Previous track (Thumb and pinky finger touching)
        if checkIfTouching(x1,y1,x4,y4,x2,y2,x3,y3,x5,y5):
                    pyautogui.press('prevtrack')
                    print("Previous Track")
                    # Create a 0.7-second delay
                    delay30(0.5)

        if checkIfTouching(x1,y1,x5,y5,x2,y2,x3,y3,x4,y4):
                    print("HAND CONTROL - OFF")
                    break

        cv2.imshow("Video", image)
        cv2.waitKey(1)

        # Can now open hurl's
        # if (xlmList[4] - xlmList[20]) < 30 & abs(ylmList[4] - ylmList[20]) < 30:
        #     webbrowser.get('chrome').open(url)

    cv2.imshow("Video", image)
    cv2.waitKey(1)
