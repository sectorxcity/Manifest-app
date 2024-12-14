import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt

# Spotify API credentials
CLIENT_ID = '3915a36b7b0842298f2db424957ad0d4'
CLIENT_SECRET = '704a178247454781b00f18ef071e7f85'
REDIRECT_URI = 'https://open.spotify.com/playlist/1JoR7wCU6v1shNIrUaVIuU?si=176f41d9050244ef'

# Authentication Scopes
SCOPES = "user-library-read playlist-modify-private playlist-read-private user-top-read"
# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPES))

# Helper Functions
def get_user_playlists():
    """Fetch and display user's playlists."""
    playlists = sp.current_user_playlists()
    for idx, playlist in enumerate(playlists['items']):
        print(f"{idx + 1}: {playlist['name']} (Tracks: {playlist['tracks']['total']})")
    return playlists['items']

def create_playlist(name, description=""):
    """Create a new private playlist."""
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id, name, public=False, description=description)
    print(f"Created playlist: {playlist['name']} (ID: {playlist['id']})")

def add_tracks_to_playlist(playlist_id, track_uris):
    """Add tracks to a playlist."""
    sp.playlist_add_items(playlist_id, track_uris)
    print("Tracks added successfully!")

def analyze_top_tracks(time_range="medium_term", limit=20):
    """
    Analyze user's top tracks.
    time_range: 'short_term' (last 4 weeks), 'medium_term' (last 6 months), 'long_term' (all time)
    """
    top_tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    track_data = []
    for track in top_tracks['items']:
        track_data.append({
            "Name": track['name'],
            "Artist": track['artists'][0]['name'],
            "Album": track['album']['name'],
            "Popularity": track['popularity']
        })
        return pd.DataFrame(track_data)
    
def plot_top_artists(time_range="medium_term", limit=10):
    """Plot user's top artists."""
    top_artists = sp.current_user_top_artists(limit=limit, time_range=time_range)
    artist_names = [artist['name'] for artist in top_artists['items']]
    popularity_scores = [artist['popularity'] for artist in top_artists['items']]

    plt.figure(figsize=(10, 6))
    plt.barh(artist_names, popularity_scores, color='skyblue')
    plt.xlabel("Popularity")
    plt.title("Top Artists")
    plt.gca().invert_yaxis()
    plt.show()

# Main Program
if __name__ == "__main__":
    print("Spotify Personal Playlist Manager & Analytics Tool")
    print("1. View Playlists")
    print("2. Create a Playlist")
    print("3. Add Tracks to a Playlist")
    print("4. Analyze Top Tracks")
    print("5. Plot Top Artists")
    choice = int(input("Choose an option (1-5): "))

if choice == 1:
        get_user_playlists()
elif choice == 2:
        name = input("Enter playlist name: ")
        description = input("Enter playlist description: ")
        create_playlist(name, description)
elif choice == 3:
        playlists = get_user_playlists()
        playlist_idx = int(input("Select a playlist by number: ")) - 1
        playlist_id = playlists[playlist_idx]['id']
        track_uris = input("Enter track URIs (comma-separated): ").split(",")
        add_tracks_to_playlist(playlist_id, track_uris)
elif choice == 4:
        time_range = input("Enter time range (short_term, medium_term, long_term): ")
        df = analyze_top_tracks(time_range)
        print(df)
elif choice == 5:
        time_range = input("Enter time range (short_term, medium_term, long_term): ")
        plot_top_artists(time_range)
else:
        print("Invalid choice.")       