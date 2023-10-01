# ETL of Spotify data from REST API

## The projest provides a script for extracting data fetched from Spotify REST API and loading into SQL Database.

The main goal of the script is to retrieve audio parameters from the analysis performed by Spotify's algorithms and load them into an SQL database for further exploration and analysis of the track's audio features.
The data is retrieved for the first 50 tracks of a given playlist. The ETL processes the data, allowing tracks to be analysed in terms of popularity and virality.
Key information processed:
* track's audio details
* track's popularity raiting
* main artist of the track

For a description of each audio feature, see the Spotify documentation:
https://developer.spotify.com/documentation/web-api/reference/get-audio-features

## Project overview
The project contains three modules:
1. extraction - provides objects for API authorization and retrieving data.
2. transformation - provides an object for cleaning data.
3. load - stores a sqlite database file; provides an object that connects to the database and loads data into it.
4. main.py - it aggregates the project flow and runs the ETL.

## How to install this project on your machine
1. Clone this project.
2. Create a file /load/credentials.py and add your credentials.To get authorization you need to follow the process described at: https://developer.spotify.com/documentation/web-api/concepts/authorization
3. To run ETL: open main.py module, assign new playlist id and run the script.
