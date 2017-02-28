# Analysis of 2000-16 NBA Most Valuable Player Data

## Overview
This project will consist of several parts:
1) Data scrape
2) Data munge
3) Visualizations
4) Analysis
5) Forecasting model
6) Projecting 2017 MVP voting


## Data

### Scrape

Data was obtained from basketball-reference.com. The following data was captured:

* Player statistic data for the 200-16 seasons
* Player advanced statistic data for the 2000-16 seasons
* MVP award voting data for the 2000-16 seasons
* Team final standings data for the 2000-16 seasons

A third piece of data that has yet to be collected:

* Player statistics for the 2017 (current) season

Basketball Reference has no scrape API that I'm aware of, but using Requests and BeautifulSoup4 to request and parse the relative data was relatively straightforward.

When scraping voting data, I noticed that the 'Rank' field in the html code was broken in the event of ties, so I rewrote that logic to simply increment by one for each record. It may later prove necessary to appropriately note ties by assigning the same ranking to those receiving the same number of points.

I had trouble scraping the 'expanded standings' table using BeautifulSoup4, which is the one I wanted for its cleanliness. I didn't spend too much time trying to determine why I was having these issues - I tried a few different parsers, but ultimately was not able to create a 'Soup' element which found this table. It appeared that none of the child elements after a commented-out child element were recognized. I'll leave it to another day to determine whether the fault here lies with myself or with the library. I was able to get the data I needed by instead retrieving data from two other standings tables, one for each conference per year. It will require some cleaning when formulating my data set later.

I'll address data quality later, but suffice it to say for now that I trust that the data I did pull is accurate.


**Relevant Code Files**: scrape.py

**Relevant Data Files**: ./scrapedata/\*.csv

### Munge

To prepare data for analysis, I'll put relevant data in a Pandas DataFrame. Our final dataset should have a record for each player season, including statistics, team performance, and MVP voting data.

* % of team's games played
* Player's team winning percentage
* Whether player's team made playoffs or not (1 or 0)

Our approach will be:
* Create a dataframe for basic and advanced statistics, then join them
* Create a dataframe for standings data, then join the relevant data to the statistics dataframe
* Create a dataframe for MVP voting data, then join the relevant data to the statistics dataframe

To help reduce noise and outliers, we will remove any players averaging less than 25 minutes per game. We will also drop any players who played for multiple teams in any season - although several such players have received MVP votes, none have come close to winning. Removing this small subset does help simplify munging later on when joining dataframe by team name. We also use a regular expression to remove '*' characters from player names.

For the standings data, we want to add additional Series' for games played (so we can determine winning percentage and, later on, percentage of games played by a player), as well as whether the team made the playoffs. We used some regular expression wrangling and a dictionary to translate full team names into three letter abbreviations. One ad-hoc fix was necessary- the original Charlotte Hornets used a different three letter identifier than the current Charlotte Hornets. Rather than iterate through different dictionaries by year, we simply replace the new acronym with the old acronym depending on the year of the series.

We want to then append the voting data to the main dataframe, adding an additional column for if the player received votes or not.

We perform these steps for each year, and merge them all together to create our final DataFrame object. We can then sort by 'Share' (share of voting points won), and drop any extraneous columns.

**Relevant Code Files**: munge.py

**Relevant Data Files**: ./output/dataframe.csv

## Analysis/Findings



## Comments

### Data Quality



## Instructions

To replicate:
1. Clone this directory to your local machine
2. Run *scrape.py* to retrieve raw data
3. Run *munge.py* to create final DataFrame and output file

**Required Software Packages/Libraries:** Python3, BeautifulSoup4, Requests, Pandas, Numpy

Or, you can just install the appropriate Anaconda package.
