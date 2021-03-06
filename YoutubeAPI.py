from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class YoutubeApi:
    def __init__(self) -> None:
        self.base_url = "https://www.googleapis.com/youtube/v3"
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", scopes=["https://www.googleapis.com/auth/youtube"]
        )

        flow.run_local_server(
            host="127.0.0.1",
            port=8888,
            prompt="consent",
            authorization_prompt_message="",
        )

        credentials = flow.credentials
        self.youtube = build("youtube", "v3", credentials=credentials)

    def create_playlist(self, playlist_name):
        make_playlist = self.youtube.playlists().insert(
            part="snippet, status",
            body={
                "snippet": {
                    "title": playlist_name,
                },
                "status": {"privacyStatus": "public"},
            },
        )
        response = make_playlist.execute()
        self.playlist_id = response["id"]
        print(f"Playlist {playlist_name} created.")
        return True

    def get_tracks_from_youtube(self, tracks):
        #  searches for youtube video which  has title similar to
        #  spotify track and returns the most relevant search result
        self.videos = []
        for track in tracks:
            search_request = self.youtube.search().list(
                part="snippet", maxResults=1, order="relevance", q=track
            )
            response = search_request.execute()
            search_result = response["items"][0]
            video_id = search_result["id"]["videoId"]
            self.title = search_result["snippet"]["title"]

            self.videos.append({
                'id': video_id,
                'title': self.title
            })
        return True

    def add_track_to_playlist(self):
        videos = self.videos
        playlist_id = self.playlist_id
        for video in videos:
            add_video = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": video['id']},
                    }
                },
            )
            print(f"Adding {video['title']} to playlist.")
            add_video.execute()

        return True
