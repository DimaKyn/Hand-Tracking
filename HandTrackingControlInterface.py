
import tkinter as tk
from tkinter import Label

import HandTrackingModule as htm
import time
import cv2
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from MethodsFile import *
import GlobalVariables as gv

import os
import pandas as pd
import spotipy
from speech_recognition import Microphone, Recognizer, UnknownValueError
from spotipy.oauth2 import SpotifyOAuth

from MethodsFile import *

import threading

import GlobalVariables as gv


class ControlClass:

    # Return whether only one finger is touching the thumb
    @staticmethod
    def checkIfTouching(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5):
        return (abs(x1 - x2) + abs(y1 - y2) < 30) \
               & (abs(x1 - x3) + abs(y1 - y3) > 60) \
               & (abs(x1 - x4) + abs(y1 - y4) > 60) \
               & (abs(x1 - x5) + abs(y1 - y5) > 60)

    # Music player hand control
    def Hand_Control(self, spotify, deviceID):
        
        # Uses the i webcam
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # tracker is a hand tracker class
        tracker = htm.handTracker()
        
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
                elif self.checkIfTouching(x1, y1, x3, y3, x2, y2, x4, y4, x5, y5) \
                        & (gv.CURR_TIME >= gv.PREV_TIME + 1):
                    spotify.next_track()
                    print("Next Track")
                    gv.CURR_OPERATION = "NEXT TRACK"

                    # Used for removing text from the screen after 3 seconds
                    gv.THREE_SECONDS_PASSED = time.time()
                    gv.PREV_TIME = gv.CURR_TIME

                # Previous track (Thumb and pinky finger touching)
                elif self.checkIfTouching(x1, y1, x4, y4, x2, y2, x3, y3, x5, y5) \
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
            
    
     # Music player hand control
    def Voice_Control(self, spotify, deviceID):
        # entry = tk.Entry(root)
        # entry.pack()
        # button = tk.Button(root, text='Submit', command=get_auth_code(auth_manager, entry, root))
        # button.pack()
        
        def show_commands(stop_event):
            
            root_thread = tk.Tk()
            label = Label(root_thread, text='Voice Control Mode', font=("Arial", 20))
            label.pack()
            label2 = Label(root_thread, text=
            'These are the available commands:\n'
            + '"Album" + name of an album - This will play the chosen album. \n'
            + '"Artist" + name of an artist - This will play the most popular tracks of the chosen artist.\n'
            + '"Play" + name of a track - This will play the chosen track.\n'
            + '"Playlist" + name of a playlist - This will play the first playlist with a corresponding name.\n'
            + '"Queue" + name of a track - This will queue a track to be played later.\n'
            + '"Language" + Russian - This will change the voice recognition to recognize Russian, (can work for different languages [see file: ChangeSearchLanguage] in this repository).\n'
            + '"Nevermind" - This will turn off Voice control mode and will switch to Hand Gesture mode.\n'
            + '"Volume" + "Max"/"Maximum"/"Half"/"Number 0-100" - This will set the volume to the desired value.', font=("Arial", 12), justify="left")
            label2.pack()
            
            def check_flag():
                if stop_event.is_set():
                    root_thread.quit()
                root_thread.after(50, check_flag)  # Check every 50 milliseconds
            check_flag()
            root_thread.mainloop()
        
        def show_recorded_command(stop_event_recorded_command):
            root_thread = tk.Tk()
            root_thread.geometry("300x200")
            label = Label(root_thread, text='Voice Control Mode', font=("Arial", 20))
            label
            label.pack()
            label3 = Label(root_thread, text=f'You said: {command}', font=("Arial", 12), justify="left")
            label3.pack()
            
            def check_flag():
                if stop_event_recorded_command.is_set():
                    time.sleep(4)
                    root_thread.quit()
                root_thread.after(50, check_flag)  # Check every 50 milliseconds
            check_flag()
            
            root_thread.mainloop()
            
        stop_event = threading.Event()
        thread_show_possible_commands = threading.Thread(target=show_commands, args=(stop_event,))
        thread_show_possible_commands.start()
                
        # Setup microphone and speech recognizer
        r = Recognizer()
        
        

        # input_mic = 'Line (2- Steinberg UR22mkII )'  # Use whatever is your desired input
        # for i, microphone_name in enumerate(Microphone.list_microphone_names()):
        #     if microphone_name == input_mic:
        #         m = Microphone(device_index=i)

        #
        # spotify.pause_playback(device_id=deviceID)
        # If there is no spotify device active, open a new spotify tab and set volume to 50%
        try:
            spotify.volume(volume_percent=10)
        except spotipy.exceptions.SpotifyException:
            os.system("start \"\" https://open.spotify.com")
        finally:
            spotify.volume(volume_percent=10)

        # Sets the default language to English
        language = "en-US"
        
        
        
        while True:
            """
            Commands will be entered in the specific format explained here:
             - the first word will be one of: 'album', 'artist', 'play'
             - then the name of whatever item is wanted
            """
            with Microphone() as source:
                print("Recording...")
                r.adjust_for_ambient_noise(source=source)
                audio = r.listen(source=source)
            
            try:
                command = r.recognize_google(audio_data=audio, language=language).lower()
                stop_event.set()
                stop_event_recorded_command = threading.Event()
                thread_show_recorded_command = threading.Thread(target=show_recorded_command, args=(stop_event_recorded_command,))
                thread_show_recorded_command.start()
                stop_event_recorded_command.set()

            except UnknownValueError:
                continue

            words = command.split()

            if len(words) <= 1:
                if words[0] == "nevermind":
                    break
                print('Could not understand. Try again')
                continue

            name = ' '.join(words[1:])
            try:
                if words[0] == 'album':
                    uri = get_album_uri(spotify=spotify, name=name)
                    play_album(spotify=spotify, device_id=deviceID, uri=uri)
                    break
                elif words[0] == 'artist':
                    uri = get_artist_uri(spotify=spotify, name=name)
                    play_artist(spotify=spotify, device_id=deviceID, uri=uri)
                    break
                elif words[0] == 'play':
                    uri = get_track_uri(spotify=spotify, name=name)
                    play_track(spotify=spotify, device_id=deviceID, uri=uri)
                    break
                elif words[0] == 'queue' or words[0] == 'q' or words[0] == 'you':
                    uri = get_track_uri(spotify=spotify, name=name)
                    queue_track(spotify=spotify, uri=uri)
                    break
                elif words[0] == "language" and words[1] == "russian":
                    language = "ru-RU"
                    continue
                elif words[0] == "language" and words[1] == "english":
                    language = "en-US"
                    continue
                elif words[0] == "playlist":
                    uri = get_playlist_uri(spotify=spotify, name=name)
                    play_playlist(spotify=spotify, device_id=deviceID, uri=uri)
                    break
                elif words[0] == "volume":
                    if words[1] == "max" or words[1] == "maximum":
                        spotify.volume(volume_percent=100)
                    elif words[1] == "half":
                        spotify.volume(volume_percent=50)
                    elif int(words[1]) <= 100 and int(words[1]) >= 0:
                        spotify.volume(volume_percent=int(words[1]))
                    return
                else:
                    print('Specify either "album", "artist", "play", "playlist", or "language". Try Again')
                    break
            except InvalidSearchError:
                print('InvalidSearchError. Try Again')
        spotify.volume(volume_percent=100)
        ######################################################


def main():
    
    # Set variables from setup.txt
    setup = pd.read_csv('setup.txt', sep='=', index_col=0, header=None)[1]
    client_id = setup['SPOTIFY_CLIENT_ID']
    client_secret = setup['SPOTIFY_CLIENT_SECRET']
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
        
    
    # root = tk.Tk()
    # label = Label(root, text='Welcome to Spotify Gesture Control')
    # label.pack()
    # label2 = Label(root, text='Login to your Spotify account and paste the browser URL here!\nIf you leave this empty, the program will try to login with the cached token.')
    # label2.pack()
    # entry = tk.Entry(root)
    # entry.pack()
    # button = tk.Button(root, text='Submit', command=get_auth_code(auth_manager, entry, root))
    # button.pack()
    # root.mainloop()
        
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    
    # Selecting device to play from
    devices = spotify.devices()
    
    print(devices)

    deviceID = None
    for d in devices['devices']:
        print(devices['devices'])
        d['name'] = d['name'].replace('’', '\'')
        if d['name'] == device_name:
            deviceID = d['id']
    
    control_class = ControlClass()

    while True:
        control_class.Hand_Control(spotify, deviceID)
        control_class.Voice_Control(spotify, deviceID)
        pass

if __name__ == "__main__":
    main()


