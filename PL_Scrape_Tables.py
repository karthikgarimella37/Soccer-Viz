import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import psycopg2 as psy
import re
import requests
from bs4 import BeautifulSoup
import seaborn as sns
import os
import datetime
import json
from urllib.request import urlopen
# from PIL import Image
# from highlight_text import fig_text
# from mplsoccer import Bumpy, FontManager, add_image
from sqlalchemy import create_engine
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS
import warnings

warnings.filterwarnings('ignore')

os.environ['AWS_ACCESS_KEY_ID'] = 'AKIA47CRW53BPNMGXUHN'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
os.environ['AWS_DEFAULT_REGION'] = 'us-west-1'

# Initialize the ApiGateway
gateway = ApiGateway('https://fbref.com/', regions = EXTRA_REGIONS)
gateway.start()

# Start session
session = requests.Session()
session.mount('https://fbref.com/', gateway)

df = pd.DataFrame()

# Looping for a set range - incremental load will be done from 2023-24 season
for i in range(1888, 2025):
    try:
        # Getting the site for each consecutive year
        
        fbref_site_url = f'https://fbref.com/en/comps/9/{i}-{i+1}/{i}-{i+1}-Premier-League-Stats#all_stats_squads_standard'
        response = session.get(fbref_site_url)
        fbref_site = response.text

        # Using pandas read_html to get the table
        fbref_table = pd.read_html(fbref_site)[0]
        fbref_table['season'] = str(i) + '/' + str(i+1)

        print(fbref_table)

        pd.concat([df, fbref_table])

        print('Data Extracted')
        
        # input()
        if "xG" in fbref_table:
            column_names = ["league_position", "club_name", "matches_played", "wins", "draws", "losses",
                        "goals_scored", "goals_conceded", "goal_difference", "points", "points_per_match",
                        "xg", "xga", "xgd", "xgd_per_90", "avg_attendance",
                        "top_team_scorer", "goalkeeper", "notes", 'season']
        else:
            column_names = ["league_position", "club_name", "matches_played", "wins", "draws", "losses",
                        "goals_scored", "goals_conceded", "goal_difference", "points", "points_per_match",
                        "avg_attendance", "top_team_scorer", "goalkeeper", "notes", 'season']
            print('Columns created')

            # Renaming columns in the DataFrame
            fbref_table = fbref_table.rename(columns=dict(zip(fbref_table.columns, column_names)))
            
            print('Table with new columns created')
            # Creating engine to connect to PostgreSQL DB
            engine = create_engine('postgresql+psycopg2://postgres:Karthik37@localhost:5432/Football')
            conn = engine.connect()



            print('Engine Created')


            # Inserting into the temp table

            if "xg" in fbref_table:
                fbref_table.to_sql('epl_league_table_tmp', conn, if_exists = 'append', index = False)
                print('Data Appened to the tmp table')
            else:
                fbref_table.to_sql('epl_league_table_tmp_no_xg', conn, if_exists = 'append', index = False)
                print('Data Appened to the tmp table')

            conn.close
    except Exception as e:
        print('Halted, Error')
        print(e)
        continue


print('Data Dump Done!')

