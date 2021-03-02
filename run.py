#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 00:42:44 2021

@author: farrasarias
"""

# Import dependencies
from requests_spotify import requests_handler
from scoring_playlists import playlist_scoring
import pandas as pd
import json
import time
from timeloop import Timeloop
from datetime import timedelta

# Define variables
data_path = "./data/"
tl = Timeloop()

# Read JSON
f = open(data_path + "promotional_playlists.json", "r")
json_data = json.load(f)
f.close()


# Code to run the app
@tl.job(interval=timedelta(seconds=43200))
def run_code():
    prom_playlists = json_data["promotion_playlists"]
    cav_playlists = json_data["caviar_playlist"]
    client_id = "bb40a0f94272480c86d31d3103840f78"
    client_secret = "30ee1a00a9b448a288f6a6e0ce60a63b"

    requests = requests_handler(prom_playlists, cav_playlists, client_id, client_secret)
    requests.connect_spotify()
    cav_info, prom_info = requests.extract_songs_info()

    time_name = data_path + "prom_playlists_" + str(int(time.time())) + ".json"

    with open(time_name, "w") as outfile:
        json.dump(prom_info, outfile, indent=4, sort_keys=True)

    scoring = playlist_scoring(cav_info, prom_info)
    df = scoring.get_all_scores()
    df.to_csv(data_path + "playlists_sorted_scores" + str(int(time.time())) + ".csv")


# Function is run once first before starting the timer
run_code()

# Start the timer to periodically ask for requests
if __name__ == "__main__":
    tl.start(block=True)
