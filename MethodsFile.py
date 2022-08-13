from spotipy import Spotify as sf


def play_album(spotify=None, device_id=None, uri=None):
    sf.start_playback(device_id=device_id, context_uri=uri)


