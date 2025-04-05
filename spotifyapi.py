import spotipy
from spotipy.oauth2 import SpotifyOAuth
import gitIgnore.spotifykeys as spotifykeys
import json

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-public",
        client_id=spotifykeys.getID(),
        client_secret=spotifykeys.getSecretID(),
        redirect_uri="http://localhost:7777/callback.",
        open_browser=False
    )
) 
spotifyPlaylist = "https://open.spotify.com/playlist/4gzwjaY1vyE5WltMC5xn8V?si=328848c4e16f437a"
playlistID = (sp.playlist(spotifyPlaylist))['id']
playlist = (sp.playlist(spotifyPlaylist))

