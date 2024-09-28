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
from urllib.parse import quote
# from PIL import Image
# from highlight_text import fig_text
# from mplsoccer import Bumpy, FontManager, add_image
from sqlalchemy import create_engine, text
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS
import warnings

warnings.filterwarnings('ignore')

os.environ['AWS_ACCESS_KEY_ID'] = 'AWS_ACCESS_KEY_ID'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'AWS_SECRET_ACCESS_KEY'
os.environ['AWS_DEFAULT_REGION'] = 'AWS_DEFAULT_REGION'

# Initialize the ApiGateway
gateway = ApiGateway('https://fbref.com/', regions = EXTRA_REGIONS)
gateway.start()

# Start session
session = requests.Session()
session.mount('https://fbref.com/', gateway)

df = pd.DataFrame()

engine = create_engine('postgresql+psycopg2://postgres:Karthik37@localhost:5432/Football')
# conn = engine.connect()

with engine.connect() as conn:
    latest_season_sql = conn.execute(text('select max(season) from epl_league_table'))
    latest_season = latest_season_sql.fetchone()[0][5:]

# Looping for a set range - incremental load will be done from 2024-25 season
for i in range(int(latest_season), datetime.datetime.now().year + 1):
    try:
        # Getting the site for each consecutive year
        
        fbref_site_url = f'https://fbref.com/en/comps/9/{i}-{i+1}/{i}-{i+1}-Premier-League-Stats#all_stats_squads_standard'
        response = session.get(fbref_site_url)
        fbref_site = response.text

        # Using pandas read_html to get the table
        fbref_table = pd.read_html(fbref_site)[0]
        fbref_table['season'] = str(i) + '/' + str(i+1)

        if 'Last 5' in fbref_table:
            fbref_table = fbref_table.drop(columns = ['Last 5'])

        if fbref_table.iloc[0]['MP'] == 0:
            break

        else:
            df = pd.concat([df, fbref_table])
        


            print('Data Extracted')

            
            # input()
            if "xG" in fbref_table.columns:
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




            print('Engine Created')


            # Inserting into the temp table

            with engine.connect() as conn:
                table_name = 'epl_league_table_tmp' if 'xg' in fbref_table.columns else 'epl_league_table_tmp_no_xg'
                fbref_table.to_sql(table_name, conn, if_exists='append', index=False)
                print(f"Data for season {i}/{i + 1} appended to {table_name}.")

            # if "xg" in fbref_table.columns:
            #     fbref_table.to_sql('epl_league_table_tmp', conn, if_exists = 'append', index = False)
            #     print('Data Appened to the tmp table')
            # else:
            #     fbref_table.to_sql('epl_league_table_tmp_no_xg', conn, if_exists = 'append', index = False)
            #     print('Data Appened to the tmp table')

            conn.close
    except Exception as e:
        print('Halted, Error')
        print(e)
        conn.close()
        continue


print('Data Dump Done!')

# To generate csv file of the database table
# df.to_csv('db_data.csv')


