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

def fpl_to_csv():
    # Navigate to FPL website
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

    # Get raw data dump from FPL website
    response = requests.get(url)
    json_blob = json.loads(response.text)

    # Get only the Player Info data blob imbedded in the response
    player_json_blob = json_blob['elements']

    position_json_blob = json_blob['element_types']
    pos_map = {}
    for pos in position_json_blob:
        print(pos['id'])
        print(pos['singular_name_short'])
        pos_map.update({pos['id'] : pos['singular_name_short']})

    team_json_blob = json_blob['teams']
    team_map = {}
    for team in team_json_blob:
        print(team['id'])
        print(team['short_name'])
        team_map.update({team['id']: team['short_name']})

    # Get just the columns that we care about
    df = pd.DataFrame(player_json_blob)
    player_df = df[['id', 'first_name', 'second_name', 'web_name', 'team', 'element_type', 'ict_index', 'points_per_game', 'selected_by_percent', 'total_points', 'minutes', 'goals_scored', 'assists', 'clean_sheets', 'bonus', 'form', 'now_cost', 'value_form', 'value_season', 'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards', 'saves']]
    #position_df = df_pos[['id', 'plural_name_short']]
    #teams_df = df_teams[['id', 'short_name']]


    # Need this in order to avoid warnings that we don't care about
    pd.options.mode.chained_assignment = None

    # Replace all team and position numerical values with their corresponding text values per pos_map and team_map
    player_df = player_df.replace({'element_type': pos_map})
    player_df = player_df.replace({'team': team_map})

    player_df.to_csv('FPL_player_data.csv', encoding='utf-8', index=False)

    # GET FIXTURE DIFFICULTY AND ADD IT ON TO THE PLAYER DF
    for index, row in player_df.iterrows():
        print('Processing player: ', row['id'])
        url = 'https://fantasy.premierleague.com/api/element-summary/' + str(row['id']) + '/'
        # use requests to get the player data in json format
        r = requests.get(url)
        json_blob = json.loads(r.text)
        # take just the fixture portion and put into Pandas DF
        fixture_json_blob = json_blob['fixtures']
        fix_df = pd.DataFrame(fixture_json_blob)
        fix_df.astype(int, errors='ignore')

        gameweek = fix_df['event'].to_list()
        try:
            gameweek = [x for x in gameweek if str(x) != 'nan']
            gameweek = list(map(int, gameweek))
            gameweek_len = len(gameweek)
            difficulty = fix_df['difficulty'].to_list()
            if len(difficulty) == len(gameweek) +1:
                difficulty.pop()
                print('OK')

        except Exception as e:
                print(e)

            # Write to a csv file so that we can have a look at it and/or import into Tableau

fpl_to_csv()
