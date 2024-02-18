

from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

# Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

test_lnk = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=77d8f5cd51cd478d"

def get_tracks_from_playlist(pl_lnk=test_lnk):
    playlist_URI = pl_lnk.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

    track_list = list()

    for track in sp.playlist_tracks(playlist_URI)["items"]:
        # Artist details
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)
        artist_name = track["track"]["artists"][0]["name"]
        artist_pop = artist_info["popularity"]
        artist_genres = artist_info["genres"]

        # Album & Track details
        album = track["track"]["album"]["name"]
        track_uri = track["track"]["uri"]
        track_name = track["track"]["name"]
        track_pop = track["track"]["popularity"]

        track_list.append((track_name, artist_name, album))

    return track_list

    