import os
import re
import pandas as pd
import numpy as np

teams = {'Atlanta Hawks':'ATL',
'Boston Celtics':'BOS',
'Brooklyn Nets':'BRK',
'Charlotte Bobcats':'CHO',
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
'New OrleansOklahoma City Hornets':'NOH',
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
    # read data into DataFrames
    pergame, advanced, voting, east, west = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    for filename in os.listdir(directory):
        if re.match(f"per_game_stats_{year}.csv", filename):
            pergame = pd.read_csv(os.path.join(directory,filename))
        elif re.match(f"advanced_stats_{year}.csv", filename):
            advanced = pd.read_csv(os.path.join(directory,filename))
        elif re.match(f"mvp_voting_{year}.csv", filename):
            voting = pd.read_csv(os.path.join(directory,filename))
        elif re.match(f"[a-z]+s_standings_E_{year}.csv", filename):
            east = pd.read_csv(os.path.join(directory,filename))
        elif re.match(f"[a-z]+s_standings_W_{year}.csv", filename):
            west = pd.read_csv(os.path.join(directory,filename))

    # assemble stats dataframe
    pergame = pergame.loc[:,['Player','Age','Tm','G','MP','TRB','AST','STL','BLK','PS/G']]
    advanced = advanced.loc[:,['Player','Age','Tm','PER','TS%','USG%']]
    stats = pd.merge(pergame, advanced, on=['Player','Age','Tm'], how='left')
    stats['Year'] = year
    # drop all duplicate rows (i.e. players who played on multiple teams in same season)
    stats = stats.drop_duplicates(subset=['Player','Age'], keep=False)
    # only keep rows for players playing 25 minutes per game or more
    stats = stats[stats.MP >= 25.0]
    # box is sum of rebounds, assists, steals, blocks
    stats['box'] = stats['TRB'] + stats['AST'] + stats['STL'] + stats['BLK']

    # assemble standings dataframe. sort so that 2017 playoff teams can be easily determined
    east = east.rename(columns = {'Eastern Conference':'Tm'}).sort_values('W/L%', ascending=False).reset_index(drop=True)
    west = west.rename(columns = {'Western Conference':'Tm'}).sort_values('W/L%', ascending=False).reset_index(drop=True)
    # this will remove the Division/Conference header lines
    standings = pd.concat([east, west]).dropna()
    standings = standings.loc[:,['Tm','W','L','W/L%']]
    standings['playoffs'] = standings['Tm'].str.contains('\*').astype(int)
    # assume playoffs for top 8 teams in each conference
    if year == 2017:
        standings['playoffs'][standings.index < 8] = 1
    standings['games'] = standings['W'] + standings ['L']
    standings['Tm'] = standings['Tm'].str.replace('[^\w\s]+','').str.replace('\d+\s*$','').str.strip()
    standings = standings.replace({'Tm':teams}, regex=True)
    # if year is < 2003 replace CHA with CHH. ugly but it works!
    if year < 2003:
        standings['Tm'].replace('CHA','CHH', inplace=True)
    standings = standings.drop(['W','L'], axis=1)
    df_merge = pd.merge(stats, standings, on='Tm', how='left')

    if not voting.empty:
    # assemble voting dataframe
        voting['Tm'] = voting['Tm'].str.strip()
        voting = voting.loc[:,['Player','Age','Tm','Share']]
        df_merge = pd.merge(df_merge, voting, on=['Player', 'Age','Tm'], how='left')
        #final cleanup of df_merge
        df_merge['got_votes'] = (df_merge['Share'] > 0).astype(int)
        df_merge['Share'].fillna(0, inplace=True)
    else:
        df_merge['got_votes'] = np.nan
        df_merge['Share']= np.nan
    df_merge['gp_pct'] = df_merge['G'] / df_merge['games']
    df_merge = df_merge.drop(['G','games'], axis=1)
    if data.empty:
        data = df_merge
    else:
        data = pd.concat([data,df_merge])

data = data.sort_values('Share', ascending=False)
# output to csv
outdir = os.path.join(os.getcwd(),'output')
if not os.path.exists(outdir):
    print(f"Creating directory \'{outdir}\'")
    os.makedirs(outdir)
data.to_csv(outdir + '/dataframe.csv', index=False)
