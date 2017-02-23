import os
import re
import pandas as pd
import numpy as np

# key is 3LA, value is team name in standings
teams = {'Dallas Mavericks':'DAL',
'Detroit Pistons':'DET',
'Indiana Pacers':'IND',
'Los Angeles Lakers':'LAL',
'Miami Heat':'MIA',
'Minnesota Timberwolves':'MIN',
'Orlando Magic':'ORL',
'Philadelphia 76ers':'PHI',
'Phoenix Suns':'PHO',
'Sacramento Kings':'SAC',
'San Antonio Spurs':'SAS',
'Seattle SuperSonics':'SEA',
'Toronto Raptors':'TOR',
'Utah Jazz':'UTA'}

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

# assemble standings dataframe
east = east.rename(columns = {'Eastern Conference':'Team'})
west = west.rename(columns = {'Western Conference':'Team'})
frames = [east, west]
# this will remove the Division/Conference header lines
standings = pd.concat(frames).dropna()
standings = standings.loc[:,['Team','W','L','W/L%']]
standings['playoffs'] = standings['Team'].str.contains('\*').astype(int)
