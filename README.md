# Spotify to Youtube Playlist Converter

Converts your playlist from spotify to youtube.

## How does it Work?
You will need to have a valid spotify and youtube account to use this. Then, you will need to configure some settings to make this script work.
Check instructions below on how configure those settings.

## Instructions:

1. Register and create an app from spotify [dashboard](https://developer.spotify.com/dashboard/). Spotify will provide you with a Client ID. 
    - In .env file copy and paste the id inside "spotify_client_id".
    - Copy the url of spotify playlist thay you want to convert and paste it in "playlist_url".
    - Inside your spoitfy application open edit settings and set Redirect URI to :```http://127.0.0.1:8000/```

2. Open [google develoeprs console](https://console.cloud.google.com/apis/credentials). 
    - Create a new project. 
    - Search for "YouTube Data API v3" in Library and enable it for your app.
    - To use this API you will need to create credentials. But before that you will need to create oauth consent.
    - On OAuth consent screen select User Type External and create.
    - Fill up the app registration form.
    - Add ../auth/youtube scope.
    - And add your email in test users.
    - Now, from Credentials, Create OAuth client ID.
    - Set application type to web application.
    - Set Authorized redirect URI: ```http://127.0.0.1:8888/```
    - An OAuth client will be created. Download the json file and move it to your working directory. And rename it to ```client_secret.json```.

3. Create a virtual environment and install requirements.
    - Create venv: ```python3 -m venv env```
    - Install requirements: ```pip install requirements.txt```
    - Activate venv: ```source env/bin/activate```
 
 4. Run the script as ```python3 playlist-converter.py```.
    - The browser will open and request for Spotify access. On granting access, you will be redirected to a different url. 
    - Copy and paste the redirected url to the console.
    - The browser will open again and ask for Youtube acces. On granting acces to youtube, it will create the playlist and songs from the spotify playlist.

## Notes:
 - Do not set redirected URI of YouTube and Spotify to the same port.
 - Make sure the ports are not being used. 
 - There is a strict limit on api request to Youtube API. You can find more about it from [here](https://developers.google.com/youtube/v3/getting-started#quota).

## Refrences:
- Spotify Authorization flow: [authorization guide](https://developer.spotify.com/documentation/general/guides/authorization-guide/
)
- [Youtube Api](https://developers.google.com/youtube/v3/getting-started)