import HandTrackingModule as htm
import time
import cv2
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from MethodsFile import *
import GlobalVariables as gv


class HandControl:

    # Return whether only one finger is touching the thumb
    @staticmethod
    def checkIfTouching(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5):
        return (abs(x1 - x2) + abs(y1 - y2) < 30) \
               & (abs(x1 - x3) + abs(y1 - y3) > 60) \
               & (abs(x1 - x4) + abs(y1 - y4) > 60) \
               & (abs(x1 - x5) + abs(y1 - y5) > 60)

    # Music player hand control
    def Hand_Control(self):
        # Uses the i webcam
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # tracker is a hand tracker class
        tracker = htm.handTracker()

        ######################################################
        # Set variables from setup.txt
        setup = pd.read_csv('setup.txt', sep='=', index_col=0, squeeze=True, header=None)

        client_id = setup['client_id']
        client_secret = setup['client_secret']
        device_name = setup['device_name']
        redirect_uri = setup['redirect_uri']
        scope = setup['scope']
        username = setup['username']

        # Connecting to the Spotify account
        auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            username=username)
        spotify = spotipy.Spotify(auth_manager=auth_manager)

        # Selecting device to play from
        devices = spotify.devices()

        deviceID = None
        for d in devices['devices']:
            print(devices['devices'])
            d['name'] = d['name'].replace('’', '\'')
            if d['name'] == device_name:
                deviceID = d['id']

        # Display image, find hands, then find their position
        while True:
            success, image = cap.read()
            image = tracker.handsFinder(image)
            lmList, xlmList, ylmList = tracker.positionFinder(image)

            gv.CURR_TIME = time.time()
            if gv.CURR_TIME <= gv.PREV_TIME + 2:
                cv2.putText(image, str(gv.CURR_OPERATION), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                            (200, 100, 200), 3)

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

                # Play music (Insures middle finger is close to ring finger) 👌
                if self.checkIfTouching(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5) \
                        & (gv.CURR_TIME >= gv.PREV_TIME + 1):
                    try:
                        pause_play(spotify=spotify, device_id=deviceID)
                        print("Pause")
                    except spotipy.exceptions.SpotifyException:
                        print("Play")
                        start_play(spotify=spotify, device_id=deviceID)

                    gv.CURR_OPERATION = "PLAY/PAUSE"

                    # Used for removing text from the screen after 3 seconds
                    gv.THREE_SECONDS_PASSED = time.time()
                    gv.PREV_TIME = gv.CURR_TIME

                # Next Track (Middle finger and thumb touching)
                if self.checkIfTouching(x1, y1, x3, y3, x2, y2, x4, y4, x5, y5) \
                        & (gv.CURR_TIME >= gv.PREV_TIME + 1):
                    spotify.next_track()
                    print("Next Track")
                    gv.CURR_OPERATION = "NEXT TRACK"

                    # Used for removing text from the screen after 3 seconds
                    gv.THREE_SECONDS_PASSED = time.time()
                    gv.PREV_TIME = gv.CURR_TIME

                # Previous track (Thumb and pinky finger touching)
                if self.checkIfTouching(x1, y1, x4, y4, x2, y2, x3, y3, x5, y5) \
                        & (gv.CURR_TIME >= gv.PREV_TIME + 1):
                    try:
                        spotify.previous_track()
                        print("Previous Track")
                    except spotipy.exceptions.SpotifyException:
                        print("No previous track")
                    gv.CURR_OPERATION = "PREVIOUS TRACK"

                    # Used for removing text from the screen after 3 seconds
                    gv.THREE_SECONDS_PASSED = time.time()
                    gv.PREV_TIME = gv.CURR_TIME

                if self.checkIfTouching(x1, y1, x5, y5, x2, y2, x3, y3, x4, y4) \
                        & (gv.CURR_TIME >= gv.PREV_TIME + 1):
                    gv.CURR_OPERATION = "VOICE CONTROL MODE"

                    # Used for removing text from the screen after 3 seconds
                    gv.THREE_SECONDS_PASSED = time.time()
                    gv.PREV_TIME = gv.CURR_TIME
                    break

                cv2.imshow("Video", image)
                cv2.waitKey(1)

            cv2.imshow("Video", image)
            cv2.waitKey(1)
