from bqspot import spotlib

def spotify_data(user, playlist):

    spotify = spotlib.create_spotify_client('bqspot/credentials/spot.json')
    top_tracks = spotlib.get_tracks(spotify, user, playlist) # Populates top tracks table
    top_artists = [track.artist_id for track in top_tracks]
    artist_information = spotlib.get_artists(spotify, top_artists) # Populates Artist information table from top tracks

    spot_data = {'tracks' : top_tracks, 'artists' : artist_information}

    return spot_data

if __name__ == "__main__":

    user = 'spotify'
    user_playlist = '37i9dQZF1DXcBWIGoYBM5M'

    data = spotify_data(user, user_playlist)
