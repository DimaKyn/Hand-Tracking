import os
import pandas as pd
import spotipy
from speech_recognition import Microphone, Recognizer, UnknownValueError
from spotipy.oauth2 import SpotifyOAuth

from MethodsFile import *


class HandControl:

    # Music player hand control
    def Hand_Control(self):
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
            d['name'] = d['name'].replace('’', '\'')
            if d['name'] == device_name:
                deviceID = d['id']

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
            spotify.volume(volume_percent=50)
        except spotipy.exceptions.SpotifyException:
            os.system("start \"\" https://open.spotify.com")
        finally:
            spotify.volume(volume_percent=50)

        # Sets the default language to English
        language = "en-US"
        while True:
            """
            Commands will be entered in the specific format explained here:
             - the first word will be one of: 'album', 'artist', 'play'
             - then the name of whatever item is wanted
            """
            with Microphone() as source:
                print("Recording")
                r.adjust_for_ambient_noise(source=source)
                audio = r.listen(source=source)

            try:
                command = r.recognize_google(audio_data=audio, language=language).lower()
                print(f"You said: {command}\n ")
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
                else:
                    print('Specify either "album", "artist", "play", "playlist", or "language". Try Again')
                    break
            except InvalidSearchError:
                print('InvalidSearchError. Try Again')

        spotify.volume(volume_percent=100)

        ######################################################
