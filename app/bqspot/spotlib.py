import spotipy
import spotipy.oauth2 as oauth2

class song(object):

    def __init__(self, artist, artist_id, name, name_id, popularity, duration, explicit, preview, features):
        self.artist = artist
        self.artist_id = artist_id
        self.name = name
        self.name_id = name_id
        self.popularity = popularity
        self.duration_ms = duration
        self.explicit = explicit
        self.preview = preview
        self.features = features

    def duration_sec(self):
        return int(round(0.001 * self.duration_ms))

class artist(object):

    def __init__(self, artist, artist_id, followers, genres, popularity, related_artists, top_tracks):
        self.artist = artist
        self.artist_id = artist_id
        self.followers = followers
        self.genres = genres
        self.popularity = popularity
        self.related_artists = related_artists
        self.top_tracks = top_tracks

    def num_related_artists(self):
        return len(self.related_artists)

    def num_top_tracks(self):
        return len(self.top_tracks)

def create_spotify_client():
    credentials = oauth2.SpotifyClientCredentials(client_id='67012152abf74f368dd6668a9ee9946e',client_secret='2ca324b8c1d14be5af1e8175d2d7961e')
    token = credentials.get_access_token()
    spotify = spotipy.Spotify(auth=token)

    return spotify

def get_tracks(client, user, playlist):

    results = client.user_playlist(user, playlist)
    items = results['tracks']['items']

    full_list = []
    for track in items:
        artist = track['track']['artists'][0]['name']
        artist_id = track['track']['artists'][0]['id']
        name = track['track']['name']
        name_id = track['track']['id']
        song_popularity = track['track']['popularity']
        duration = track['track']['duration_ms']
        explicit = track['track']['explicit']
        preview_url = track['track']['preview_url']
        features = client.audio_features(name_id)[0]

        temp_song_obj = song(artist, artist_id, name, name_id, song_popularity, duration, explicit, preview_url, features)
        full_list.append(temp_song_obj)

    return full_list

def get_artists(client, artist_ids):

    artist_list = []

    for artist_id in artist_ids:
        results = client.artist(artist_id)

        name = results['name']
        followers = results['followers']['total']
        genres = results['genres']
        popularity = results['popularity']
        related_artists = get_related_artists(client, artist_id)
        artists_top_tracks = [result['name'] for result in client.artist_top_tracks(artist_id, 'US')['tracks']]

        temp_artist_obj = artist(name, artist_id, followers, genres, popularity, related_artists, artists_top_tracks)
        artist_list.append(temp_artist_obj)

    return artist_list

def get_related_artists(client, artist_id):

    all_related_results = client.artist_related_artists(artist_id)
    related_artists = [artists['name'] for artists in all_related_results['artists']]

    return related_artists
