# spotify_playlist_scoring
A simple python app to extract playlist information from Spotify to score the importance of promotional playlists.

## How to use

- Please make sure to install al the dependencies in the requirements.txt file.
- Run the run.py code to start the app.
- The code is currently fixed to run every 12 hours, provided the run.py code keeps running in a server.

## Overview

The requests_spotify.py file contains the necessary methods to request spotify tokens and make all the necessary requests to the API. It also contains the methods necessary to parse and extract the necessary data.

The scoring_playlists.py file contains the methods to compare the Caviar playlist with the other promotional playlists and decide upon a score.

The score calculation is simple. If the promotional playlist posted a song 3 days before it appeared on Caviar, then a number 3 will be added to the playlist score. This calculation is made this way to give more weight to the playlist who have had the song for longer periods of time. If a playlist uploaded a song less than a day away from Caviar, it probably didn't contribute to the popularity of the song.

## Output

The app outputs a .json storing all the relevant info extracted and parsed from Spotify.

Also, it outputs a .csv with the ordered list of playlists according to their scoring.

Both of these outputs happen every 12 hours for the time being. This should potentially be linked to a database to be stored there.

Two sample output files have been placed on the data folder for reference purposes.
