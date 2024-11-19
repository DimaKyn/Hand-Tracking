# Spotify-Hand-Tracking-And-Voice-Control

******Work In Progress******

Imagine washing the dishes or cooking something and having your hands wet or full of chunks of food, you could ask google voice control to play some music, but good luck playing something else cause the microphone can't hear you while its playing.
This is the exact reason I made this software.

This code combines Mediapipe's api for hand tracking, the Spotipy API and Jake Goodman's (Youtube: Jake Goodman/Github: https://github.com/jakegoodman01/Pepper) code to create a software which allows the control of Spotify using hand gestures and voice control, with added features.

Upon running this software, your default camera will turn on along with a window displaying what the camera captures.
If the software runs for the first time, a tab will be opened, copy the link in your browser and paste it to the console/terminal (This will authorize your Spotify account with the software).

Instructions:
1. Download this repository.
2. Go to https://developer.spotify.com/dashboard
3. Create a new app > "Name it however you'd like"
4. Go to Settings, and paste https://localhost:8888/callback in the "Redirect" input box.
5. Now go to Settings > Copy SPOTIFY_CLIENT_SECRET and SPOTIFY_CLIENT_ID.
6. Paste both SPOTIFY_CLIENT_SECRET and SPOTIFY_CLIENT_ID in the file "setup.txt" in the project directory.
7. Install Python 3.
8. Run the following code in your terminal to install all required dependencies:
```
pip install opencv-python mediapipe spotipy pandas SpeechRecognition PyAudio
```
5. Run the "HandTrackingControlInterface.py" file to start the program.
6. You will be navigated to a certain link in your default browser.
7. If you are not logged in to your spotify account on your browser, you will be required to login.
8. Copy and paste the link you were directed to by the software and paste it inside the UI.
9. Once you press on the "Submit" button, your spotify account will be authenticated with this program.
10. Hold your hand directly in front of the camera in the "High five" position.
11. Touching the thumb with different fingers executes different commands:

   Index finger - Play/Pause.

   Middle finger - Next track.

   Ring finger - Previous track.

   Pinky finger - Voice control (Allows you to search for playlists/artists/tracks using your voice)
  
4. Upon entering Voice control, the volume will lower and hand gestures will turn off until you say a command, here are the possible commands:

   "album" + *name of an album* - This will play the chosen album.
   
   "artist" + *name of an artist* - This will play the most popular tracks of the chosen artist.
   
   "play" + *name of a track* - This will play the chosen track.
   
   "playlist" + *name of a playlist* - This will play the first playlist with a corresponding name.
   
   "queue" + *name of a track* - This will queue a track to be played later.
   
   "language" + *Russian* - This will change the voice recognition to recognize Russian, (can work for different languages [see file: ChangeSearchLanguage] in this repository).
   
   "nevermind" - This will turn off Voice control mode and will switch to Hand Gesture mode.

   "Volume" + Number/"Half"/"Max"/"Maximum" - This will set the volume to your desired value.
