"""
Module provides connection to the Spotify API.
"""
import requests
from api_authorization import ApiAuthorization


class DataExtractor:
    """
    Class connects to the API.
    Provides set of functions allowing fetching data from Spotify.
    """

    def __init__(self) -> None:
        self.auth = ApiAuthorization()
        self.token = self.auth.get_refreshed_token()

    def get_playlist_items(self, playlist_id: str) -> dict:
        """
        Gets items of an playlist.

        Parameters
        ----------
        playlist_id: str
            ID of a Spotify playlist
        """
