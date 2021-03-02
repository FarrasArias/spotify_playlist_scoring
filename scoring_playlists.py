#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 00:38:19 2021

@author: farrasarias
"""

import pandas as pd
import numpy as np
import json
import time


# This class manages the scoring of the playlists
class playlist_scoring:
    def __init__(self, caviar_relevant_info, promotion_relevant_info):
        self.cav_info = caviar_relevant_info
        self.prom_info = promotion_relevant_info

    # This function determines the score the playlist will have based on the time difference
    # between the Caviar added time and the playlist added time.
    def count_songs_added_before(self, intersection, prom_key):
        if not intersection:
            return 0
        else:
            score = 0
            for id in intersection:
                time_difference = np.datetime64(self.cav_info[id][0], "D") - np.datetime64(
                    self.prom_info[prom_key][id][0], "D")
                time_int = time_difference.astype(int)

                if time_int > 0:
                    score += time_int
        return score

    def get_all_scores(self):
        prom_keys = list(self.prom_info.keys())
        prom_scores = []
        for key in prom_keys:
            prom_playlist_keys = list(self.prom_info[key].keys())
            cav_keys = list(self.cav_info.keys())
            intersection = np.intersect1d(prom_playlist_keys, cav_keys)
            score = self.count_songs_added_before(intersection, key)
            prom_scores.append(score)

        df = pd.DataFrame([prom_keys, prom_scores]).T
        df = df.sort_values(by=[1], ascending=False)
        return df
