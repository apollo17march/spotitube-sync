# SpotiTube Sync: Spotify to YouTube Music Playlist Converter 🎵🔄📺

## Introduction 🌟

Are you a YouTube Music subscriber who feels left out when your friends share their awesome Spotify playlists? 😢 Fear not! SpotiTube Sync is here to bridge the gap between these two popular music streaming platforms. 🎉

Spotify is renowned for its superior playlist curation and sharing capabilities. However, YouTube Music subscribers often find themselves unable to directly import these playlists. SpotiTube Sync solves this problem by effortlessly transferring your favorite Spotify playlists to YouTube Music, ensuring you never miss out on great music recommendations! 🚀🎧

## Features ✨

- 🔐 Secure authentication with Spotify and YouTube
- 🔍 Fetches tracks from Spotify playlists
- 🎵 Creates a new playlist on YouTube Music
- 🔄 Searches and adds tracks to YouTube Music playlist
- ⏳ Handles rate limiting to ensure smooth transfers
- 🎨 User-friendly command-line interface with emoji feedback

## Prerequisites 📋

1. Spotify Developer Account and API Credentials
2. Google Cloud Project with YouTube Data API v3 enabled
3. Python 3.6+

## Installation 🛠️

1. Clone the repository:
```
git clone https://github.com/apollo17march17/spotitube-sync.git
cd spotitube-sync
```

2. Install required packages:
```
pip install -r requirements.txt
```

3. Set up your Spotify and YouTube credentials (see Credentials Setup section below)


## Usage 🚀
Run the script:
```
python spotitube_sync.py
```

Follow the prompts to enter your Spotify playlist link and authenticate with both Spotify and YouTube.

## Credentials Setup 🔑

### Spotify API Credentials

1. Create a Spotify Developer account at https://developer.spotify.com/
2. Log in and navigate to the Dashboard
3. Click on "Create an App"
4. Fill in the app name and description, then click "Create"
5. In your app's settings, find your Client ID and Client Secret
6. Add `http://localhost:8888/callback` to the Redirect URIs in your app settings
7. Save these credentials in your `.env` file:
```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```

### YouTube Data API v3 Credentials

1. Create a Google Cloud Project
    - Go to the [Google Cloud Console](https://console.cloud.google.com/)
    - Sign in with your Google account
    - Click on the project dropdown (top-left corner) and select "New Project"
    - Enter a project name and click "Create"
    - Select your new project from the project dropdown

2. Enable YouTube Data API v3
    - In the Google Cloud Console, go to "APIs & Services" > "Library"
    - Search for "YouTube Data API v3"
    - Click on the API and then click "Enable"

3. Create OAuth 2.0 Credentials
    - Go to "APIs & Services" > "Credentials"
    - Click "Create Credentials" and select "OAuth client ID"
    - If prompted, configure the OAuth consent screen:
    - Choose "External" user type (or "Internal" if you have a Google Workspace account)
    - Fill in the required fields (App name, User support email, Developer contact information)
    - You can skip optional fields for now
    - Add the scope: `../auth/youtube` (for managing YouTube account)
    - Add test users if you're using external user type
    - For application type, select "Desktop app"
    - Give your client ID a name
    - Click "Create"

4. Download and Place Credentials
    - After creating the credentials, you'll see a dialog with your Client ID and Client Secret
    - Click "Download JSON"
    - Save this file as `client_secret.json` in your project directory

5. Use Credentials in the Script
    - Ensure `client_secret.json` is in the same directory as your script
    - The script will use this file for YouTube authentication

By completing these steps, you'll have the necessary credentials to access both the Spotify API and the YouTube Data API v3, allowing SpotiTube Sync to transfer playlists between the platforms.


## Contributing 🤝

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/apollo17march/spotitube-sync/issues).

## License 📄

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

## Acknowledgements 👏

- Spotify API
- YouTube Data API v3
- [Spotipy](https://github.com/plamere/spotipy)
- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
