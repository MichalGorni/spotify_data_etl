"""
Module provides connection to the Spotify API.
"""
import requests
from extraction.api_authorization import ApiAuthorization
from datetime import date


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
        self.current_date = date.today().strftime("%Y-%m-%d")

    def get_playlist_items(self, playlist_id: str) -> list[dict]:
        """
        Gets items of an playlist.

        Parameters
        ----------
        playlist_id: str
            ID of a Spotify playlist

        Returns
        -------
        playlist_items: list containing dictionary/es
            Dictionary with playlist items.
            dict = {
                playlist_id: int,
                track_id: int,
                order: int,
                playlist_number_of_tracks: int
                date_fetched: str
            }
        """
        limit = 50
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit={limit}"
        response = requests.get(url=url, headers=self.headers)
        data: dict = response.json()
        # data["playlist_id"] = playlist_id
        total: int = data["total"]
        playlist_items: list[dict] = []
        for index, item in enumerate(data["items"], start=1):
            track = {
                "playlist_id": playlist_id,
                "track_id": item["track"]["id"],
                "track_order": index,
                "playlist_number_of_tracks": total,
                "date_fetched": self.current_date,
            }
            playlist_items.append(track)
        return playlist_items

    def get_playlist_details(self, playlist_id: str) -> list:
        """
        Gets details of given id playlist.

        Parameters
        ----------
        playlist_id: str
            ID of playlist to be searched.

        Returns
        -------
        playlist_details: list
            List object containing dictionary with playlist details

        """
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        response = requests.get(url=url, headers=self.headers)
        data: dict = response.json()
        playlist_details = {
            "playlist_id": playlist_id,
            "name": data["name"],
        }
        return [playlist_details]

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
        track_data["popularity"] = self.get_track_popularity(track_id=track_id)
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

    def get_several_track_audio_features(self, track_ids: list) -> list[dict]:
        """
        Gets audio details for several tracks in one API call.

        Parameters
        ---------
        track_ids: list
            List containing IDs of tracks.

        Returns
        -------
        tracks_data: list
            list containing dictionaries with single track audio features
        """
        tracks = ",".join(track_ids)
        url = rf"https://api.spotify.com/v1/audio-features?ids={tracks}"
        response = requests.get(
            url,
            headers=self.headers,
        )
        tracks_data = response.json()["audio_features"]
        return tracks_data

    def get_several_track_details(self, track_ids: list) -> tuple[list[dict]]:
        """
        Function fetches details for multiple tracks

        Parameters
        ---------
        track_ids: list
            List objects with string items representing IDs of tracks.

        Returns
        -------
        tracks_data: list
            list containing dictionaries, each cotaining a single track details
        """
        ids = ",".join(track_ids)
        url = rf"https://api.spotify.com/v1/tracks?ids={ids}"
        response = requests.get(
            url,
            headers=self.headers,
        )
        tracks = response.json()["tracks"]
        track_artist_bridge: list[dict] = []
        track_details: list[dict] = []
        for track in tracks:
            # creating dictionary containing details of a track
            track_data: dict = {}
            track_data["track_id"] = track["id"]
            track_data["name"] = track["name"]
            track_data["popularity"] = track["popularity"]
            track_data["album_id"] = track["album"]["id"]
            track_data["main_artist_id"] = track["artists"][0]["id"]
            # creating dictionary representing track - artist connection
            # in case of multiple artist
            for artist in track["artists"]:
                connection = {"track_id": track["id"], "artist_id": artist["id"]}
                track_artist_bridge.append(connection)
            track_details.append(track_data)

        return track_details, track_artist_bridge
