import requests, base64, hashlib, secrets, string
from urllib.parse import urlparse, parse_qs
import webbrowser
from decouple import config
from os.path import split


class SpotifyApi:
    def __init__(self) -> None:
        self.client_id = config("client_id")
        self.base_url = "https://accounts.spotify.com"
        self.redirect_uri = "http://127.0.0.1:8888/"
        self.spotify_api= f"https://api.spotify.com/v1/playlists"

    def create_code_verifier_challenge(self):
        code_verifier = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(50, 100))
        hash_code_verifier = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(hash_code_verifier).rstrip(b"=").decode()
        return code_verifier, code_challenge

    def open_authorize_url(self):
        self.state = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10,15))
        self.code_verifier, code_challenge = self.create_code_verifier_challenge()
        scope = "playlist-modify-public playlist-read-collaborative"
        uri = f"{self.base_url}/authorize?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope={scope}&state={self.state}&code_challenge_method=S256&code_challenge={code_challenge}"
        r = requests.get(uri)
        return webbrowser.open(r.url)
    
    def perform_authorization(self, auth_redirect_uri):
        parsed_url = urlparse(auth_redirect_uri)[4]
        url_query = parse_qs(parsed_url)        
        code = url_query.get("code")
        error = url_query.get("error")
        state = url_query['state']
        
        if error is not None or self.state != state[0]:
            print(error[0])
            return False
        
        self.token_url = f"{self.base_url}/api/token"       
        request_body = {
            "client_id": self.client_id,
            "grant_type": "authorization_code",
            "code": code[0],
            "redirect_uri": self.redirect_uri,
            "code_verifier": self.code_verifier
        }
        r = requests.post(self.token_url, data=request_body)
        self.response_data = r.json()
        return True


    def get_playlist_items(self):
        access_token = self.response_data['access_token']
        header = {
            "Authorization": f"Bearer {access_token}"
        }
        playlist_url = config("playlist_url")
        playlist_path = urlparse(playlist_url).path
        self.playlist_id = split(playlist_path)[1]
        playlist_items_url = f"{self.spotify_api}/{self.playlist_id}/tracks"
        r = requests.get(playlist_items_url, headers=header)
        response = r.json()
        playlist_items = response['items']
        return playlist_items
    
    def get_track_names_from_playlist_items(self):
        playlist_items = self.get_playlist_items()
        track_names = []
        for playlist_item in playlist_items:
            artists = [artist['name'] for artist in playlist_item['track']['artists']]
            for artist in artists:
                track_name = playlist_item['track']['name'] + " " + artist
                print(f"Fetching {playlist_item['track']['name']} from spotify.")
            track_names.append(track_name)
        return track_names

    def get_playlist_name(self):
        access_token = self.response_data['access_token']
        playlist_id = self.playlist_id
        header = {
            "Authorization": f"Bearer {access_token}"
        }
        r = requests.get(f"{self.spotify_api}/{playlist_id}", headers=header)
        data = r.json()
        playlist_name = data['name']
        return playlist_name