from bqspot import spotlib, bqlib
from google.cloud import bigquery

def spotify_data(path, user, playlist):

    spotify = spotlib.create_spotify_client(path)
    top_tracks = spotlib.get_tracks(spotify, user, playlist) # Populates top tracks table
    top_artists = [track.artist_id for track in top_tracks]
    artist_information = spotlib.get_artists(spotify, top_artists) # Populates Artist information table from top tracks

    tracks_table_data = []
    features_table_data = []
    artist_table_data = []
    genre_table_data = []
    top_artist_tracks_table_data = []
    related_artists_table_data = []


    for track in top_tracks:
        temp_tracks = (track.artist,
                       track.artist_id,
                       track.name,
                       track.name_id,
                       track.popularity,
                       track.explicit,
                       track.preview,
                       track.duration_sec())
        tracks_table_data.append(temp_tracks)

    for features in top_tracks:
        temp_features = (features.features['id'],
                         features.features['danceability'],
                         features.features['energy'],
                         features.features['key'],
                         features.features['loudness'],
                         features.features['mode'],
                         features.features['speechiness'],
                         features.features['acousticness'],
                         features.features['instrumentalness'],
                         features.features['liveness'],
                         features.features['valence'],
                         features.features['tempo'])

        features_table_data.append(temp_features)

    for artist in artist_information:
        temp_artists = (artist.artist,
                        artist.artist_id,
                        artist.followers,
                        artist.popularity
                        )

        artist_table_data.append(temp_artists)

    for artist in artist_information:
        for genre in artist.genres:
            temp_genre = (artist.artist_id,
                          genre
                          )
            genre_table_data.append(temp_genre)

    for artist in artist_information:
        for top_track in artist.top_tracks:
            temp_top_tracks = (artist.artist_id,
                               top_track
                               )
            top_artist_tracks_table_data.append(temp_top_tracks)

    for artist in artist_information:
        for related_artist in artist.related_artists:
            temp_related_artists = (artist.artist_id,
                               related_artist
                               )
            related_artists_table_data.append(temp_related_artists)

    spot_data = [{"name" : "tracks", "data" : tracks_table_data},
                 {"name" : "features", "data" : features_table_data},
                 {"name" : "artists", "data" : artist_table_data},
                 {"name" : "genres", "data" : genre_table_data},
                 {"name" : "top_artist_tracks", "data" : top_artist_tracks_table_data},
                 {"name" : "related_artists", "data" : related_artists_table_data}
                 ]

    return spot_data

def bq_creation(creds_path, data):
    bqclient = bqlib.create_bq_client(creds_path)

    dataset_name = "spotify_dataset"

    tracks_schema = [
        bigquery.SchemaField('artist', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('artist_id', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('name', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('name_id', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('popularity', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('explicit', 'BOOLEAN', mode='NULLABLE'),
        bigquery.SchemaField('preview', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('duration_sec', 'INTEGER', mode='NULLABLE')
    ]

    features_schema = [
        bigquery.SchemaField('name_id', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('danceability', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('energy', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('key', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('loudness', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('mode', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('speechiness', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('acousticness', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('instrumentalness', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('liveness', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('valence', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('tempo', 'FLOAT', mode='NULLABLE')
    ]

    artists = [
        bigquery.SchemaField('artist', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('artist_id', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('followers', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('popularity', 'FLOAT', mode='NULLABLE'),
    ]

    genres = [
        bigquery.SchemaField('artist_id', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('genre', 'STRING', mode='NULLABLE')
    ]

    top_artist_tracks_schema = [
        bigquery.SchemaField('artist_id', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('name', 'STRING', mode='NULLABLE')
    ]

    related_artists_schema = [
        bigquery.SchemaField('artist_id', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('related_name', 'STRING', mode='NULLABLE')
    ]

    table_struct = [{'name' : 'tracks', 'schema' : tracks_schema},
                    {'name' : 'features', 'schema' : features_schema},
                    {'name' : 'artists', 'schema' : artists},
                    {'name' : 'genres', 'schema' : genres},
                    {'name' : 'top_artist_tracks', 'schema' : top_artist_tracks_schema},
                    {'name' : 'related_artists', 'schema' : related_artists_schema},
                    ]

    bqlib.create_taxonomy(bqclient, dataset_name, table_struct)
    bqlib.load_data(bqclient, data, dataset_name)



if __name__ == "__main__":

    user = 'spotify'
    user_playlist = '37i9dQZF1DXcBWIGoYBM5M'
    spot_path = 'bqspot/credentials/spot.json'
    bq_path = 'bqspot/credentials/bq_key.json'

    data = spotify_data(spot_path, user, user_playlist)
    bq_creation(bq_path, data)
