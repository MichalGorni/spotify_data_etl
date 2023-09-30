"""
Modules contains Token class representing refreshed OAuth toke.
Most of the authorization has been done in the past.
Only token refreshment needed.
"""

import requests

# importing secret credentials needed for Spotify API authorization
from extraction import credentials


class ApiAuthorization:
    """
    Class refreshes authorization token need for connection to the API.
    Uses secret client credentials.
    """

    def __init__(self) -> None:
        pass

    def get_refreshed_token(self) -> str:
        """
        Refreshes authorization token.

        Returns
        -------
        token: str
            string variable representing OAuth token.
        """
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": f"Basic {credentials.BASE64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        body = {
            "grant_type": "refresh_token",
            "refresh_token": credentials.REFRESH_TOKEN,
        }
        response = requests.post(url, headers=headers, data=body)
        token = response.json()
        return token["access_token"]
