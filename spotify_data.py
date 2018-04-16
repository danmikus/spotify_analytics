import spotipy
import spotipy.oauth2 as oauth2
from pprint import pprint


def create_client():
    credentials = oauth2.SpotifyClientCredentials(client_id='67012152abf74f368dd6668a9ee9946e',client_secret='2ca324b8c1d14be5af1e8175d2d7961e')
    token = credentials.get_access_token()
    spotify = spotipy.Spotify(auth=token)

    return spotify

def get_tracks(client):
    name = "Today's Top Hits"
    results = spotify.user_playlist('spotify','37i9dQZF1DXcBWIGoYBM5M')
    items = results['tracks']['items']

    full_list = []
    for track in items:
        artist = track['track']['artists'][0]['name']
        artist_id = track['track']['artists'][0]['id']
        name = track['track']['name']
        name_id = track['track']['id']
        popularity = track['track']['popularity']

        print(artist, artist_id, name, name_id, popularity)

#        song_dict = {'artist_name' : artist,
#                     'id' : artist_id,
#                     }

#        full_list.append(song_dict)

    return full_list

if __name__ == "__main__":
    spotify = create_client()
    get_tracks(spotify)



# Genre
# Number of Followers
# popularity of artists
# artists picture?
