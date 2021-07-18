from os import access
import requests, base64, hashlib, secrets, string
from urllib.parse import urlparse, parse_qs
import webbrowser
from decouple import config
from datetime import datetime, timedelta
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
        self.response_data  = r.json()
        self.token_expiry_time = datetime.now() + timedelta(seconds=self.response_data['expires_in'])
        return True
    
    def get_access_token(self):
        data = self.response_data
        access_token = data['access_token']
        now = datetime.now()
        if now > self.token_expiry_time:
            request_body = {
                "grant_type": "refresh_token",
                "refresh_token": data['refresh_token'],
                'client_id': self.client_id
            }
            r = requests.post(self.token_url, data=request_body)
            access_token = r.json()['access_token']
        return access_token


    def get_playlist_items(self):
        access_token = self.get_access_token()
        header = {
            "Authorization": f"Bearer {access_token}"
        }
        playlist_url = config("playlist_url")
        playlist_path = urlparse(playlist_url).path
        playlist_id = split(playlist_path)[1]
        playlist_items_url = f"{self.spotify_api}/{playlist_id}/tracks?limit=10"
        r = requests.get(playlist_items_url, headers=header)
        playlist_items = r.json()
        print(playlist_items)
        return playlist_items
        
        
if __name__ == "__main__":
    s = SpotifyApi()
    s.open_authorize_url()
    auth_redirect_uri = input("Copy and paste the url you were redirected to here.\n")
    s.perform_authorization(auth_redirect_uri=auth_redirect_uri)
    s.get_playlist_items()
    

    
