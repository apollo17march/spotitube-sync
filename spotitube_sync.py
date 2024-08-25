import spotipy
from spotipy.oauth2 import SpotifyOAuth
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from tqdm import tqdm
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI', 'http://localhost:8888/callback')
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube"]
YOUTUBE_CLIENT_SECRETS_FILE = "client_secret.json"

def authenticate_spotify():
    print("\n🔑 Authenticating with Spotify...")
    sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope="playlist-read-private")
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    print("✅ Spotify authentication successful.\n")
    return sp

def get_spotify_playlist_tracks(sp, playlist_link, playlist_name):
    print("Retrieving Spotify playlist tracks...\n")
    playlist_id = playlist_link.split('/')[-1].split('?')[0]
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    for item in results['items']:
        track = item['track']
        tracks.append(f"{track['name']} {track['artists'][0]['name']}")
    print(f"Tracks retrieved from Spotify playlist ▶️{playlist_name}▶️:")
    print("\n".join(f"  🎵 {track}" for track in tracks))
    print("")
    return tracks

def authenticate_youtube():
    print("🔑 Authenticating with YouTube...\n")
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
    credentials = flow.run_local_server(port=5555)
    youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)
    print("✅ YouTube authentication successful.\n")
    return youtube

def check_if_playlist_exists(youtube, title):
    print("🔍 Checking if YouTube playlist already exists...\n")
    request = youtube.playlists().list(
        part="snippet",
        mine=True,
        maxResults=50
    )
    response = request.execute()
    
    for item in response.get('items', []):
        if item['snippet']['title'] == title:
            print(f"⚠️ Playlist '{title}' already exists on YouTube.\n")
            return item['id']
    return None

def create_youtube_playlist(youtube, title, description=""):
    print(f"🆕 Creating new YouTube playlist: {title}...\n")
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    )
    response = request.execute()
    print(f"✅ Created YouTube playlist '{title}' with ID: {response['id']}.\n")
    return response['id']

def search_and_add_tracks_youtube(youtube, track_list, playlist_id):
    print("🎶 Adding tracks to YouTube playlist...\n")
    for track in tqdm(track_list, desc="Processing tracks"):
        try:
            tqdm.write(f"🔎 Searching for track: {track}")
            request = youtube.search().list(
                part="snippet",
                maxResults=1,
                q=track
            )
            response = request.execute()
            if response['items']:
                video_id = response['items'][0]['id']['videoId']
                youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id
                            }
                        }
                    }
                ).execute()
                tqdm.write(f"✅ Added track '{track}' to playlist.")
            else:
                tqdm.write(f"❌ Could not find a video for track: '{track}'")

            time.sleep(1)  # Adding delay to avoid hitting rate limits

        except googleapiclient.errors.HttpError as e:
            tqdm.write(f"⚠️ An error occurred:")
            if e.resp.status in [429, 503, 403]:  # Handling rate limit exceeded or service unavailable errors
                tqdm.write("  ⏳ Rate limit exceeded or service unavailable. Halting the process.")
                return

    print("\n🎉 Playlist transferred successfully! 🎉\n")

def transfer_playlist(spotify_link):
    sp = authenticate_spotify()
    
    try:
        playlist_id = spotify_link.split('/')[-1].split('?')[0]
        playlist_name = sp.playlist(playlist_id)['name']
        tracks = get_spotify_playlist_tracks(sp, spotify_link, playlist_name)

        youtube = authenticate_youtube()
        youtube_playlist_id = check_if_playlist_exists(youtube, playlist_name)
        if not youtube_playlist_id:
            youtube_playlist_id = create_youtube_playlist(youtube, playlist_name)

        search_and_add_tracks_youtube(youtube, tracks, youtube_playlist_id)
        print("\n🎉 Playlist transferred successfully! 🎉\n")
    except googleapiclient.errors.HttpError as e:
        print(f"\n⚠️ An error occurred: ")
        if e.resp.status == 403 and "quotaExceeded" in str(e):
            print("  ⏳ You have exceeded your YouTube quota. Please try again later.")
        else:
            print("  ⛔️ The transfer process encountered an error.")
            print(f"\nError detail: \n{e}")

if __name__ == "__main__":
    try:
        spotify_playlist_link = input("🔗 Enter Spotify playlist link: ")
        transfer_playlist(spotify_playlist_link)
    except KeyboardInterrupt:
        print("\n😢 Transfer interrupted. Goodbye! 👋")
