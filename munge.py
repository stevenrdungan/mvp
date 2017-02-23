import os
import re
import pandas as pd
year = 2000
for filename in os.listdir("/Users/stevendungan/mvp/scrapedata"):
    # read voting data into dataframe
    if re.match(f"mvp_voting_{year}.csv", filename):
        print(f"Voting file is {filename}")
    # read standings data into dataframe
    elif re.match(f"[a-z]+s_standings_E_{year}.csv", filename):
        print(f"East standings file is {filename}")
    elif re.match(f"[a-z]+s_standings_W_{year}.csv", filename):
        print(f"West standings file is {filename}")
