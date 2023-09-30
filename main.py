"""
Module running ETL pipeline.
"""
import time

from extraction.api_connection import DataExtractor
from transformation.transformation import Transformers
from load.database_connection import DataBaseConnector

extractor = DataExtractor()
transformer = Transformers()
db_connection = DataBaseConnector()


def run_etl_for_playlist(playlist_id: str) -> None:
    start = time.perf_counter()
    print("Fetching and transforming data...")
    # playlist_track table
    playlist_items = extractor.get_playlist_items(playlist_id=playlist_id)
    df_playlist_tracks = transformer.transform_playlist_tracks(playlist_items)

    # playlist_details table
    playlist_details = extractor.get_playlist_details(playlist_id=playlist_id)
    df_playlist_details = transformer.transform_playlist_details(playlist_details)

    # track_details table and track_artist_bridge table
    ids = []
    for track in playlist_items:
        ids.append(track["track_id"])
    track_details, artist_tracks_bridge = extractor.get_several_track_details(ids)
    df_track_details = transformer.transform_track_details(track_details)
    df_track_artist_bridge = transformer.transform_track_artist_bridge(
        artist_tracks_bridge
    )

    # track_audio_features table
    audio_details = extractor.get_several_track_audio_features(ids)
    df_track_audio_details = transformer.transform_track_audio_details(audio_details)

    # loading dataframes into database
    data_connection = {
        df_playlist_tracks: "playlist_tracks",
        df_playlist_details: "playlist_details",
        df_track_details: "track_details",
        df_track_artist_bridge: "track_artist_bridge",
        df_track_audio_details: "track_audio_features",
    }
    for df, table_name in data_connection.items():
        print(f"Loading data into {table_name} table")
        db_connection.load_table_to_database(df=df, table_name=table_name)
    stop = time.perf_counter()
    print(f"Done\nProcess took {round((stop-start),2)} seconds")
