import time
import HandTrackingModule as htm
import mediapipe as mp
import cv2
import pyautogui
import webbrowser
import numpy as np

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
        # Ring finger coordinates at first bend from the top
        x4_2, y4_2 = xlmList[16], ylmList[16]
        # Little finger
        x5, y5 = xlmList[20], ylmList[20]

        print(abs(x1 - x2) + abs(y1 - y2) < 50 & abs(x3 - x2) + abs(y3 - y2) > 50)
        print()
        # Play music (Insures middle finger is close to ring finger) 👌
        if abs(x1 - x2) + abs(y1 - y2) < 80 & abs(x3 - x2) + abs(y3 - y2) > 50:
            pyautogui.press('playpause')
            print("PLAY")

        # Previous track
        if abs(x1 - x5) + abs(y1 - y5) < 80 & abs(x1 - x2) + abs(y1 - y2) > 50:
            pyautogui.press('prevtrack')
            print("Previous Track")

        # Next Track
        if abs(x1 - x3) + abs(y1 - y3) < 80 & abs(x1 - x2) + abs(y1 - y2) > 50:
            pyautogui.press('nexttrack')
            print("Previous Track")


        # Can now open url's
        # if (xlmList[4] - xlmList[20]) < 30 & abs(ylmList[4] - ylmList[20]) < 30:
        #     webbrowser.get('chrome').open(url)

    cv2.imshow("Video", image)
    cv2.waitKey(1)
