import os
import re
import pandas as pd
import numpy as np

# key is 3LA, value is team name in standings
# it is okay if there are duplicate values, because
# they will never arise in the same season
# e.g. Charlotte Hornets, Charlotte Bobcats
teams = {'Atlanta Hawks':'ATL',
'Boston Celtics':'BOS',
'Charlotte Bobcats':'CHA',
'Charlotte Hornets':'CHA',
'Chicago Bulls':'CHI',
'Cleveland Cavaliers':'CLE',
'Dallas Mavericks':'DAL',
'Denver Nuggets':'DEN',
'Detroit Pistons':'DET',
'Golden State Warriors':'GSW',
'Houston Rockets':'HOU',
'Indiana Pacers':'IND',
'Los Angeles Clippers':'LAC',
'Los Angeles Lakers':'LAL',
'Memphis Grizzlies':'MEM',
'Miami Heat':'MIA',
'Milwaukee Bucks':'MIL',
'Minnesota Timberwolves':'MIN',
'New Jersey Nets':'NJN',
'New Orleans Hornets':'NOH',
'New Orleans Pelicans':'NOP',
'New York Knicks':'NYK',
'Oklahoma City Thunder':'OKC',
'Orlando Magic':'ORL',
'Philadelphia 76ers':'PHI',
'Phoenix Suns':'PHO',
'Portland Trail Blazers':'POR',
'Sacramento Kings':'SAC',
'San Antonio Spurs':'SAS',
'Seattle SuperSonics':'SEA',
'Toronto Raptors':'TOR',
'Utah Jazz':'UTA',
'Vancouver Grizzlies':'VAN',
'Washington Wizards':'WAS'}


data = pd.DataFrame()   # this will be our dataset
directory = os.path.join(os.getcwd(),'scrapedata')

for year in range(2000,2017):
    voting, east, west = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    for filename in os.listdir(directory):
        # read voting data into dataframe
        if re.match(f"mvp_voting_{year}.csv", filename):
            voting = pd.read_csv(os.path.join(directory,filename))
        # read standings data into dataframe
        elif re.match(f"[a-z]+s_standings_E_{year}.csv", filename):
            east = pd.read_csv(os.path.join(directory,filename))
        elif re.match(f"[a-z]+s_standings_W_{year}.csv", filename):
            west = pd.read_csv(os.path.join(directory,filename))

    # assemble standings dataframe
    east = east.rename(columns = {'Eastern Conference':'Tm'})
    west = west.rename(columns = {'Western Conference':'Tm'})
    frames = [east, west]
    # this will remove the Division/Conference header lines
    standings = pd.concat(frames).dropna()
    standings = standings.loc[:,['Tm','W','L','W/L%']]
    standings['playoffs'] = standings['Tm'].str.contains('\*').astype(int)
    standings['games'] = standings['W'] + standings ['L']
    standings['Tm'] = standings['Tm'].str.replace('[^\w\s]+','').str.replace('\d+\s*$','').str.strip()
    standings = standings.replace({'Tm':teams}, regex=True)

    voting['Tm'] = voting['Tm'].str.strip()
    # drop records for players without team (i.e. players who were traded midseason)
    voting = voting[voting.Tm !='TOT']
    voting_merge = pd.merge(voting, standings, on='Tm', how='left')
    voting_merge['gp_pct'] = voting_merge['G'] / voting_merge['games']
    if data.empty:
        data = voting_merge
    else:
        frames = [data,voting_merge]
        data = pd.concat(frames)

data = data.sort_values('Share', ascending=False)
data = data.drop(['Rank','First','Pts Won','Pts Max','W','L','games'], axis=1).reset_index(drop=True)

# output to csv
outdir = os.path.join(os.getcwd(),'output')
if not os.path.exists(outdir):
    print(f"Creating directory \'{outdir}\'")
    os.makedirs(outdir)
data.to_csv(outdir + '/dataframe.csv')
