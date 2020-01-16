#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 11:13:23 2019

@author: douglas
"""
# Import the libraries we need
import pandas as pd
import requests
import json

# Navigate to FPL website
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

# Get raw data dump from FPL website
response = requests.get(url)
json_blob = json.loads(response.text)

# Get only the Player Info data blob imbedded in the response
player_json_blob = json_blob['elements']
df = pd.DataFrame.from_dict(player_json_blob)

# Get just the columns that we care about
player_df = df[['id','first_name','second_name','web_name','team','element_type','ict_index','points_per_game','selected_by_percent','total_points','minutes','goals_scored','assists','clean_sheets','bonus']]

# Write to a csv file so that we can have a look at it and/or import into Tableau
player_df.to_csv('FPL_player_data.csv', encoding='utf-8')

