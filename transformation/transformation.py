import pandas as pd


class Transformers:
    """
    Provides set of functions for data transformation.
    """

    def __init__(self) -> None:
        pass

    def transform_track_details(self, data: list[dict]) -> pd.DataFrame:
        """
        - Transforms given data into a DataFrame.
        - Ensures correct data types.
        - Removes blank rows.
        Parameters
        ----------
        data: list
            List containing dictionaries representing single track data
        Returns
        -------
        df: pd.DataFrame
            DataFrame object with tracks details
        """
        data_types = {
            "track_id": str,
            "name": str,
            "popularity": int,
            "album_id": str,
            "main_artist_id": str,
        }
        df = pd.DataFrame(data)
        df = df.astype(data_types)
        df = df.dropna()
        return df

    def transform_track_artist_bridge(self, data: list[dict]) -> pd.DataFrame:
        """
        - Transforms given data into a DataFrame.
        - Ensures correct data types.
        - Removes blank rows.

        Parameters
        ----------
        data: list
            List containing dictionaries representing single track data

        Returns
        -------
        df: pd.DataFrame
            DataFrame object with tracks details
        """
        data_types = {"track_id": str, "artist_id": str}
        df = pd.DataFrame(data)
        df = df.astype(data_types)
        df = df.dropna(how="all")
        return df

    def transform_playlist_tracks(self, data: list[dict]) -> pd.DataFrame:
        """
        - Transforms given data into a DataFrame.
        - Ensures correct data types.
        - Removes blank rows.
        - Get's number of songs on playlist

        Parameters
        ----------
        data: list
            List containing dictionaries representing single track data

        Returns
        -------
        df: pd.DataFrame
            DataFrame object with tracks details
        """
        data_types = {
            "playlist_id": str,
            "track_id": str,
            "track_order": int,
            "date_fetched": "datetime64[ns]",
        }
        df = pd.DataFrame(data)
        # retreiving number of songs
        self.total_songs = df["playlist_number_of_tracks"][0]
        df = df.drop(columns=["playlist_number_of_tracks"])
        df = df.astype(data_types)
        df = df.dropna(how="all")
        return df

    def transform_playlist_details(self, data: list[dict]) -> pd.DataFrame:
        """
        - Transforms given data into a DataFrame.
        - Ensures correct data types.
        - Removes blank rows.

        Parameters
        ----------
        data: list
            List containing dictionaries representing single track data

        Returns
        -------
        df: pd.DataFrame
            DataFrame object with tracks details
        """
        data_types = {"playlist_id": str, "name": str, "total_songs": int}
        df = pd.DataFrame(data)
        df["total_songs"] = self.total_songs
        df = df.astype(data_types)
        df = df.dropna(how="all")
        return df

    def transform_track_audio_details(self, data: list[dict]) -> pd.DataFrame:
        """
        - Transforms given data into a DataFrame.
        - Ensures correct data types.
        - Removes not used columns from DataFrame.
        - Removes blank rows.

        Parameters
        ----------
        data: list
            List containing dictionaries representing single track data

        Returns
        -------
        df: pd.DataFrame
            DataFrame object with tracks details
        """
        data_types = {
            "danceability": float,
            "energy": float,
            "key": int,
            "loudness": float,
            "mode": int,
            "speechiness": float,
            "acousticness": float,
            "instrumentalness": float,
            "liveness": float,
            "valence": float,
            "tempo": float,
            "type": str,  # to be deleted
            "id": str,
            "uri": str,  # to be deleted
            "track_href": str,  # to be deleted
            "analysis_url": str,  # to be deleted
            "duration_ms": int,
            "time_signature": int,
        }
        df = pd.DataFrame(data)
        df = df.astype(data_types)
        df = df.drop(columns=["type", "uri", "track_href", "analysis_url"])
        df.insert(0, "id", df.pop("id"))
        df = df.dropna(how="all")
        return df
