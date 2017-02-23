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

**Relevant Data Files**: ./scrapedata/\*.py

### Munge

To prepare data for analysis, I'll put relevant data in a Pandas DataFrame. This DataFrame should be composed of Series' for each record in the MVP award voting data. In addition to the fields already present for each player record, the following fields need to be appended:

* Year of season
* Player's team winning percentage
* Whether player's team made playoffs or not (1 or 0)

**Relevant Code Files**: munge.py

**Relevant Data Files**:

## Analysis/Findings



## Comments

### Data Quality



## Instructions

To replicate:
1. Clone this directory to your local machine
2. Run *scrape.py* to retrieve raw data

**Required Software Packages/Libraries:** Python3, BeautifulSoup4, Requests

Or, you can just download the appropriate Anaconda package.
