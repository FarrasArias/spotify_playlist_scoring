#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 00:36:13 2021

@author: farrasarias
"""

import spotipy
import numpy as np


# This class provides functions to make requests to the spotify api.
# It also provides functions to parse and extract the required info.
class requests_handler:
    def __init__(self, promotion_playlists, caviar_playlist, client_id, client_secret):
        self.promotion_playlists = self.strip_playlists(promotion_playlists)
        self.caviar_playlist = caviar_playlist
        self.client_id = client_id
        self.client_secret = client_secret
        self.spotify = None

    def strip_playlists(self, playlist):
        return [playlist.split("playlist/")[1] for playlist in playlist]

    def connect_spotify(self):
        client_manager = spotipy.oauth2.SpotifyClientCredentials(self.client_id, self.client_secret)
        self.spotify = spotipy.Spotify(client_credentials_manager=client_manager)

    def get_items(self, id):
        return self.spotify.playlist(id)["tracks"]["items"]

    def extract_all_items(self):
        playlists_items = {id: self.get_items(id) for id in self.promotion_playlists}
        caviar_items = {id: self.get_items(id) for id in [self.caviar_playlist]}
        return playlists_items, caviar_items

    def extract_song_info(self, info):
        info_matrix = [info["track"]["uri"], info["added_at"], info["track"]["name"]]
        return info_matrix

    def extract_songs_info(self):
        playlists_items, caviar_items = self.extract_all_items()
        caviar_key = list(caviar_items.keys())[0]
        caviar_relevant_info = {}
        for info in caviar_items[caviar_key]:
            extract_info = self.extract_song_info(info)
            caviar_relevant_info[extract_info[0]] = [extract_info[1], extract_info[2]]
        promotion_keys = list(playlists_items.keys())
        promotion_relevant_info = {}
        for id in promotion_keys:
            info_dict = {}
            for playlist in playlists_items[id]:
                try:
                    song_info = self.extract_song_info(playlist)
                    info_dict[song_info[0]] = [song_info[1], song_info[2]]
                except:
                    print("Ignoring song, data not found")
            promotion_relevant_info[id] = info_dict

        return caviar_relevant_info, promotion_relevant_info
