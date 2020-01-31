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
    teams_df = df_teams[['id', 'name', 'short_name', 'strength', 'strength_overall_home', 'strength_overall_away', 'strength_attack_home', 'strength_attack_away', 'strength_defence_home', 'strength_defence_away']]
    # Need this in order to avoid warnings that we don't care about
    pd.options.mode.chained_assignment = None

    # Convert the datatypes of two columns to int so we can replace them with better values
    player_df['team'] = player_df.team.astype(int)
    player_df['element_type'] = player_df.element_type.astype(int)

    # Create maps to replace team and position values with meaningful values (team maps will need updated yearly)
    ########################################################################################
    # REPLACE THESE WITH DICTIONARY SERIES FROM DATAFRAMES ABOVE FOR TEAMS AND POSITIONS !!!
    ########################################################################################
    position_map = {1: "GK", 2: "DEF", 3: "MID", 4: "FWD"}
    team_map = {1: "ARS", 2: "AVL", 3: "BOU", 4: "BHA", 5: "BUR", 6: "CHE", 7: "CRY", 8: "EVE", 9: "LEI", 10: "LIV", 11: "MCI", 12: "MUN", 13: "NEW", 14: "NOR", 15: "SHU", 16: "SOU", 17: "TOT", 18: "WAT", 19: "WHU", 20: "WOL"}

    player_df = player_df.replace({'element_type': position_map})
    player_df = player_df.replace({'team': team_map})

    ########################
    # COMBINE THE DATAFRAMES
    ########################

    ###################################################################################################
    # GET FIXTURE DIFFICULTY HERE AND EITHER EXPORT AS SEPARATE .CSV FILE OR ADD IT ON TO THE PLAYER DF
    ###################################################################################################

    # Write to a csv file so that we can have a look at it and/or import into Tableau
    player_df.to_csv('FPL_player_data.csv', encoding='utf-8', index=False)

fpl_to_csv()