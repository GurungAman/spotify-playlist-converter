import requests, base64, hashlib, secrets, string
from urllib.parse import urlparse, parse_qs
import webbrowser
from decouple import config


class SpotifyApi:
    def __init__(self) -> None:
        self.client_id = config("client_id")
        self.base_url = "https://accounts.spotify.com"

    def create_code_verifier_challenge(self):
        code_verifier = ''.join(secrets.choice(string.ascii_uppercase + string.digits + "." + "~" + "-") for _ in range(50))
        challenge_sha256 = hashlib.sha256(code_verifier.encode('utf-8')).hexdigest()
        challenge_base64_encoded = base64.b64encode(challenge_sha256.encode()).decode()
        challenge = challenge_base64_encoded

        return code_verifier, challenge

    def open_authorize_url(self):
        redirect_uri = "http://127.0.0.1:8888/"
        self.state = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(10))

        _, code_challenge = self.create_code_verifier_challenge()
        scope = "playlist-modify-public playlist-read-collaborative"

        uri = f"{self.base_url}/authorize?response_type=code&client_id={self.client_id}&redirect_uri={redirect_uri}&scope={scope}&state={self.state}&code_challenge_method=S256&code_challenge={code_challenge}"
        r = requests.get(uri)
        return webbrowser.open(r.url)
    
    def get_token(self, redirect_uri):
        parsed_url = urlparse(redirect_uri)[4]
        url_query = parse_qs(parsed_url)
        
        code = url_query.get("code")
        error = url_query.get("error")
        state = url_query['state']
        if error is not None or self.state != state:
            print(error)
            return 
          
        
if __name__ == "__main__":
    s = SpotifyApi()
    s.open_authorize_url()
    redirect_uri = input("Copy and paste the url you were redirected to here.\n")
    s.get_token(redirect_uri=redirect_uri)

    
