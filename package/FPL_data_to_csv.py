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
    df = pd.DataFrame(player_json_blob)
    position_json_blob = json_blob['element_types']
    df_pos = pd.DataFrame(position_json_blob)
    team_json_blob = json_blob['teams']
    df_teams = pd.DataFrame(team_json_blob)

    # Get just the columns that we care about
    player_df = df[['id', 'first_name', 'second_name', 'web_name', 'team', 'element_type', 'ict_index', 'points_per_game', 'selected_by_percent', 'total_points', 'minutes', 'goals_scored', 'assists', 'clean_sheets', 'bonus', 'form', 'now_cost', 'value_form', 'value_season', 'goals_conceded', 'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards', 'saves']]
    position_df = df_pos[['id', 'plural_name_short']]
    teams_df = df_teams[['id', 'short_name']]
    merge1_df = pd.merge(player_df, position_df, left_on='element_type', right_on='id', how='inner', suffixes=('_left','_right'))
    table = pd.merge(merge1_df, teams_df, left_on='team', right_on='id', how='inner')

    ################################################
    # Rename/drop columns so that only one ID exists
    ################################################

    # Need this in order to avoid warnings that we don't care about
    pd.options.mode.chained_assignment = None

    ###################################################################################################
    # GET FIXTURE DIFFICULTY AND ADD IT ON TO THE PLAYER DF
    ###################################################################################################
    for index, row in table.iterrows():
        print('Processing player: ', table['id'])
        url = 'https://fantasy.premierleague.com/api/element-summary/' + str(table['id']) + '/'
        # use requests to get the player data in json format
        r = requests.get(url).json()
        # take just the fixture portion and put into Pandas DF
        fix_df = pd.DataFrame(r['fixtures'])
        fix_df.astype(int, errors='ignore')

        try:
            difficulty = df[['event', 'difficulty']]
            # print(table)
        except Exception as e:
            print('Problem with ', player)
            print(e)
            print(table)
            continue

        try:
            fixture = 'GW' + str(int(row['event']))
            except Exception as e:
                print(e)
                # Write to a csv file so that we can have a look at it and/or import into Tableau
    player_df.to_csv('FPL_player_data.csv', encoding='utf-8', index=False)

fpl_to_csv()