import os
import re
import pandas as pd
import numpy as np

# key is 3LA, value is team name in standings
teams = {'DAL':'Dallas Mavericks',
'DET':'Detroit Pistons',
'IND':'Indiana Pacers',
'LAL':'Los Angeles Lakers',
'MIA':'Miami Heat',
'MIN':'Minnesota Timberwolves',
'ORL':'Orlando Magic',
'PHI':'Philadelphia 76ers',
'PHO':'Phoenix Suns',
'SAC':'Sacramento Kings',
'SAS':'San Antonio Spurs',
'SEA':'Seattle SuperSonics',
'TOR':'Toronto Raptors',
'UTA':'Utah Jazz'}

year = 2000 # change this to loop through range!
directory = "/Users/stevendungan/mvp/scrapedata"
voting, east, west = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

for filename in os.listdir("/Users/stevendungan/mvp/scrapedata"):
    # read voting data into dataframe
    if re.match(f"mvp_voting_{year}.csv", filename):
        voting = pd.read_csv(os.path.join(directory,filename))
    # read standings data into dataframe
    elif re.match(f"[a-z]+s_standings_E_{year}.csv", filename):
        east = pd.read_csv(os.path.join(directory,filename))
    elif re.match(f"[a-z]+s_standings_W_{year}.csv", filename):
        west = pd.read_csv(os.path.join(directory,filename))
