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
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": rf"Bearer {self.token}",
        }

    def get_playlist_items(self, playlist_id: str) -> dict:
        """
        Gets items of an playlist.

        Parameters
        ----------
        playlist_id: str
            ID of a Spotify playlist
        """
        pass

    def get_audio_features(self, track_id: str) -> dict:
        """
        Fetches audio features from Spotfiy API.
        Returns dictionary with audio analysis details.

        Parameters
        ----------
        track_id: str
            ID of a track to be searched

        Returns
        -------
        data: dict
         data = {
            'danceability': float,
            'energy': float,
            'key': int,
            'loudness': float,
            'mode': int,
            'speechiness': float,
            'acousticness': float,
            'instrumentalness': float,
            'liveness': float,
            'valence': float,
            'tempo': float,
            'type': str,
            'id': str,
            'uri': str,
            'track_href': str,
            'analysis_url': str,
            'duration_ms': int,
            'time_signature': int,
            'track_id': str,
            'popularity':int
            }
        """
        url = rf"https://api.spotify.com/v1/audio-features/{track_id}"
        response = requests.get(
            url,
            headers=self.headers,
        )
        track_data: dict = response.json()
        track_data["track_id"] = track_id
        track_data["popularity"] = self.get_track_popularity()
        return track_data

    def get_track_popularity(self, track_id: str) -> int:
        """
        Gets track popularity rating from Spotify API.

        Parameters
        ----------
        trakc_id: str
            ID of a track to be searched

        Returns
        -------
        popularity: int
            The popularity of a track is a value between 0 and 100, with 100 being the most popular.
        """
        url = rf"https://api.spotify.com/v1/tracks/{track_id}"
        response = requests.get(
            url,
            headers=self.headers,
        )

        data = response.json()
        popularity: int = data["popularity"]
        return popularity


if __name__ == "__main__":
    ex = DataExtractor()
    pop = ex.get_track_popularity(track_id="5kXco3VQGGmTwHpKILv1om")
    print(pop)
