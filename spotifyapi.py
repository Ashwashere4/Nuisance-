import spotipy
from spotipy.oauth2 import SpotifyOAuth
import gitIgnore.spotifykeys as spotifykeys
import json

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-public",
        client_id=spotifykeys.getID(),
        client_secret=spotifykeys.getSecretID(),
        redirect_uri="http://localhost:7777/callback."
    )
) 
spotifyPlaylist = "https://open.spotify.com/playlist/0uSVUHhS11fBhDaJd9YoY6?si=4ad3057b7cc84580"
playlistID = (sp.playlist(spotifyPlaylist))['id']
playlist = (sp.playlist(spotifyPlaylist))
test = sp.playlist(spotifyPlaylist)


# print(test)

json_string = json.dumps(test, 
                         skipkeys=False,
                         allow_nan = True, 
                         indent = 6)


