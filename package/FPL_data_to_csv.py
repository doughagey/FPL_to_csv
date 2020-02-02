#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Feb 2 2020

@author: douglas hagey
https://github.com/doughagey/FPL_to_csv
https://douglashagey4.wixsite.com/mysite
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

    # Get only a subset of the Player Info json blob imbedded in the response
    player_json_blob = json_blob['elements']

    # Create a map of positions using their id and shortname
    position_json_blob = json_blob['element_types']
    pos_map = {}
    for pos in position_json_blob:
        print(pos['id'])
        print(pos['singular_name_short'])
        pos_map.update({pos['id'] : pos['singular_name_short']})

    # Create a map of teams using their id and shortname
    team_json_blob = json_blob['teams']
    team_map = {}
    for team in team_json_blob:
        print(team['id'])
        print(team['short_name'])
        team_map.update({team['id']: team['short_name']})

    # Get just the columns that we care about
    df = pd.DataFrame(player_json_blob)
    player_df = df[['id', 'first_name', 'second_name', 'web_name', 'team', 'element_type', 'ict_index', 'points_per_game', 'selected_by_percent', 'total_points', 'minutes', 'goals_scored', 'assists', 'clean_sheets', 'bonus', 'form', 'now_cost', 'value_form', 'value_season', 'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards', 'saves']]

    # Need this bit in order to avoid warnings that we don't care about
    pd.options.mode.chained_assignment = None

    # Replace all team and position numerical values in player dataframe with their corresponding values per pos_map and team_map (otherwise they just list meaningless numbers
    player_df = player_df.replace({'element_type': pos_map})
    player_df = player_df.replace({'team': team_map})
    player_df.sort_values('id', axis=0, ascending=True, inplace=True, na_position='last')
    player_df.to_csv('FPL_player_data.csv', encoding='utf-8', index=False)

    # GET FIXTURE DIFFICULTY AND ADD IT ON TO THE PLAYER DF
    fixture_df = pd.DataFrame()
    for index, row in player_df.iterrows():
        player = row['id']
        print('Processing player: ', player)
        url = 'https://fantasy.premierleague.com/api/element-summary/' + str(player) + '/'
        # Use requests to get the player data in json format
        r = requests.get(url)
        json_blob = json.loads(r.text)
        # Take just the fixture info and put into Pandas Dataframe
        fixture_json_blob = json_blob['fixtures']
        fix_df = pd.DataFrame(fixture_json_blob)
        fix_df.astype(int, errors='ignore')
        gameweek = fix_df['event'].to_list()
        try:
            # Filter out rows that have no gameweek info
            gameweek = [x for x in gameweek if str(x) != 'nan']
            gameweek = list(map(int, gameweek))
            gameweek_len = len(gameweek)
            gameweek = map(str, gameweek)
            gameweek = ['GW' + x for x in gameweek]
            difficulty = fix_df['difficulty'].to_list()
            if len(difficulty) == len(gameweek) +1:
                difficulty.pop()
            # Combine gameweek number and difficulty into one dictionary
            fixture_list = dict(zip(gameweek, difficulty))
            fixture_list['id'] = player
            # Add row for player to include fixture listing and player_id
            fixture_df = fixture_df.append(fixture_list, ignore_index=True)
        except Exception as e:
                print(e)

    # Sort columns so they're in alphabetical order
    fixture_df = fixture_df.reindex(sorted(fixture_df.columns), axis=1)

    # Write to a csv file so that we can have a look at it and/or import into Tableau
    fixture_df.to_csv('FPL_fixture_list.csv', encoding='utf-8', index=False)

# Allows users to just run this file as a script vs importing the function into a separate python script
fpl_to_csv()
