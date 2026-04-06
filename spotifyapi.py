import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app_token import SPOTIFYTOKEN, SPOTIFYSECRET

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-public playlist-modify-private",
        cache_path = ".spotify_cache",
        client_id=SPOTIFYTOKEN,
        client_secret=SPOTIFYSECRET,
        redirect_uri="http://127.0.0.1:7777/callback",
        open_browser=False
    )
) 
spotifyPlaylist = "https://open.spotify.com/playlist/0dDDFVhe7xzNFUxVsKXTCW?si=y3A69WBKSFqfYDBNdaJ4DA"
playlistID = (sp.playlist(spotifyPlaylist))['id']
playlist = (sp.playlist(spotifyPlaylist))

