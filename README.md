# Hand-Tracking

This code combines Mediapipe's api for hand tracking, the Spotipy API and Jake Goodman's (Youtube: Jake Goodman/Github: https://github.com/jakegoodman01/Pepper) code to create a software which allows the control of Spotify using hand gestures and voice control, with added features.

Upon running this software, your default camera will turn on along with a window displaying what the camera captures.
If the software runs for the first time, a tab will be opened, copy the link in your browser and paste it to the console/terminal (This will authorize your Spotify account with the software).

Instructions:
1. Run the "HandControlInterface.py" file to start the program.
2. Hold your hand directly in front of the camera in the "High five" position.
3. Touching the thumb with different fingers executes different commands:

   Index finger - Play/Pause.

   Middle finger - Next track.

   Ring finger - Previous track.

   Pinky finger - Voice control (Allows you to search for playlists/artists/tracks using your voice)
  
4. Upon entering Voice control, the volume will halve and hand gestures will turn off until you say a command, here are the possible commands:

   "album" + *name of an album* - This will play the chosen album.
   
   "artist" + *name of an artist* - This will play the most popular tracks of the chosen artist.
   
   "play" + *name of a track* - This will play the chosen track.
   
   "playlist" + *name of a playlist* - This will play the first playlist with a corresponding name.
   
   "queue" + *name of a track* - This will queue a track to be played later.
   
   "language" + *Russian* - This will change the voice recognition to recognize Russian, (can work for different languages [see file: ChangeSearchLanguage] in this repository).
   
   "nevermind" - this will turn off Voice control mode and will switch to Hand Gesture mode.
