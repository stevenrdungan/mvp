# Forecasting the 2017 NBA MVP

## Overview




## Data

### Scrape

Data was obtained from basketball-reference.com. The following data was captured:

* MVP award voting data for the 2000-16 seasons
* Team final standings data for the 200-16 seasons

A third piece of data that has yet to be collected:

* Player statistics for the 2017 (current) season

Basketball Reference has no scrape API that I'm aware of, but using Requests and BeautifulSoup4 to request and parse the relative data was relatively straightforward.

When scraping voting data, I noticed that the 'Rank' field in the html code was broken in the event of ties, so I rewrote that logic to simply increment by one for each record. It may later prove necessary to appropriately note ties by assigning the same ranking to those receiving the same number of points.

I had trouble scraping the 'expanded standings' table using BeautifulSoup4, which is the one I wanted for its cleanliness. I didn't spend too much time trying to determine why I was having these issues - I tried a few different parsers, but ultimately was not able to create a 'Soup' element which found this table. It appeared that none of the child elements after a commented-out child element were recognized. I'll leave it to another day to determine whether the fault here lies with myself or with the library. I was able to get the data I needed by instead retrieving data from two other standings tables, one for each conference per year. It will require some cleaning when formulating my data set later.

I'll address data quality later, but suffice it to say for now that I trust that the data I did pull is accurate.


**Relevant Code Files**: scrape.py

**Relevant Data Files**: ./scrapedata/\*.csv

### Munge

To prepare data for analysis, I'll put relevant data in a Pandas DataFrame. This DataFrame should be composed of Series' for each record in the MVP award voting data. In addition to the fields already present for each player record, the following fields need to be appended:

* % of team's games played
* Player's team winning percentage
* Whether player's team made playoffs or not (1 or 0)

A 'voting' file looks like:
> Rank,Player,Age,Tm,First,Pts Won,Pts Max,Share,G,MP,PTS,TRB,AST,STL,BLK,FG%,3P%,FT%,WS,WS/48
> 1,Shaquille O'Neal,27,LAL,120.0,1207.0,1210,0.998,79,40.0,29.7,13.6,3.8,0.5,3.0,.574,.000,.524,18.6,.283
> 2,Kevin Garnett,23,MIN,0.0,408.0,1210,0.337,81,40.0,22.9,11.8,5.0,1.5,1.6,.497,.370,.765,11.6,.172

A 'standings' file looks like:
> Eastern Conference,W,L,W/L%,GB,PS/G,PA/G,SRS
> Atlantic Division
> Miami Heat* (2),52,30,.634,—,94.4,91.3,2.75
> New York Knicks* (3),50,32,.610,2.0,92.1,90.7,1.30
> Philadelphia 76ers* (5),49,33,.598,3.0,94.8,93.4,1.02

We can create a DataFrame of the voting data, to which we will append additional fields, as well as DataFrames for each of the standings data files.

For each of the 'standings' DataFrames, we can modify each record:
* Append a 'games' column by adding wins and losses
* Append a 'win_pct' column by dividing wins by games
* Append a 'playoffs' column, using 1 if a team name has an asterisk, 0 if not
* Use regular expression parsing to truncate a team's name to remove non-alphanumeric characters, except separating spaces

We can also do some cleaning of the 'voting' DataFrame:
* remove any records for players with a team of 'TOT' (indicating they played for multiple teams that season)
Then, merge these two DataFrames. Once we have our formulated 'standings' DataFrames, we can alter the 'voting' DataFrame as follows:
* Append the columns we created in our 'standings' DataFrames, joining using a dictionary to match team acronym (e.g. 'LAL') to team name ('Los Angeles Lakers')
* Create a 'pct_games' field by dividing player games played by total team games

Do this for each year, and merge them to create our final DataFrame object. We can then sort by 'Share' (share of voting points won), and drop any extraneous columns.

**Relevant Code Files**: munge.py

**Relevant Data Files**: ./output/\dataframe.csv

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
