import cv2
import mediapipe as mp
import time


class handTracker():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon

        # Mediapipe hands
        self.mpHands = mp.solutions.hands

        # hands is a Hands object
        # Hands(Keep tracking when no hand is found[T/F],maxNumOfHands INT,...
        # ...,minimum detection confidence FLOAT, minimum tracking confidence FLOAT)
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)
        # Method for drawing lines between every dot on the hand
        self.mpDraw = mp.solutions.drawing_utils

    def handsFinder(self, image, draw=True):
        # Image object
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # "process" is a method which processes the image of the camera
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                # Draw lines between landmarks
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    def positionFinder(self, image, handNo=0, draw=True):
        lmlist = []
        xlmlist = []
        ylmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]

            # id = index of finger landmark
            # Print landmark locations by pixels on the screen
            for id, lm in enumerate(Hand.landmark):
                h, w, c = image.shape
                # Position of center of the image
                cx, cy = int(lm.x * w), int(lm.y * h)
                # Lists location of each landmark on the screen
                xlmlist.append(cx)
                ylmlist.append(cy)
                lmlist.append([id, cx, cy])
                # Draw a circle on each hand landmarks
                if draw:
                    cv2.circle(image, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

        return lmlist, xlmlist, ylmlist
