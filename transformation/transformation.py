import pandas as pd


class Transformers:
    """
    Provides set of functions for data transformation.
    """

    def __init__(self) -> None:
        pass

    def transform_track_details(data: list) -> pd.DataFrame:
        data_types = {
            "track_id": str,
            "name": str,
            "popularity": int,
            "album_id": str,
            "main_artist_id": "datetime64[ns]",
        }
        df = pd.DataFrame(data)
        df = df.astype(data_types)
