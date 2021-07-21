from requests.api import patch
from SpotifyAPI import SpotifyApi
from YoutubeAPI import YoutubeApi

if __name__ == "__main__":
    spotify = SpotifyApi()

    spotify.open_authorize_url()
    auth_redirect_uri = input("Copy and paste the url you were redirected to here.\n")
    spotify.perform_authorization(auth_redirect_uri=auth_redirect_uri)
    print("\n")
    spotify_tracks = spotify.get_track_names_from_playlist_items()
    playlist_name = spotify.get_playlist_name()


    youtube = YoutubeApi()
    youtube.create_playlist(playlist_name=playlist_name)
    print("\n")
    youtube.get_tracks_from_youtube(tracks=spotify_tracks)
    youtube.add_track_to_playlist()
    