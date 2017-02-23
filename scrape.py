from bs4 import BeautifulSoup
import requests
import csv


def get_response(url):
    print(f"Requesting \'{url}\'")
    try:
        r = requests.get(url)
        text = r.text
        return BeautifulSoup(text, 'lxml')
    except requests.exceptions.RequestException as e:
        print(e)
    return None
        
# scrape MVP voting data 2000-16
for year in range(2000,2017):
    data = []
    url = f"http://www.basketball-reference.com/awards/awards_{year}.html"
    # r = requests.get(url)
    # text = r.text
    # soup = BeautifulSoup(text,"lxml")
    soup = get_response(url)
    if not soup:
        continue
    table = soup.find('table', attrs={'id':'mvp'})
    table_head = table.find('thead')
    hrow = table_head.find_all('tr')[1]
    hcols = hrow.find_all('th')
    hcols = [ele.text.strip() for ele in hcols]
    data.append([ele for ele in hcols if ele])
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    # because the 'Rank' column is broken we'll do it ourselves
    rank = 0
    for row in rows:
        rank += 1
        line = [rank]
        cols = [ele.text.strip() for ele in row.find_all('td')]
        line += [ele for ele in cols]
        data.append([ele for ele in line if ele])
    fname = f"/Users/stevendungan/mvp/scrapedata/mvp_voting_{year}.csv"
    with open(fname, 'w') as file:
        wr = csv.writer(file)
        wr.writerows(data)

# scrape standings data 2000-16
for year in range(2000,2017):
    url = f"http://www.basketball-reference.com/leagues/NBA_{year}_standings.html"
    soup = get_response(url)
    tables = soup.find_all('table')
    for table in tables:
        tid = table.get('id')
        data = []
        table_head = table.find('thead')
        hrow = table_head.find('tr')
        hcols = hrow.find_all('th')
        hcols = [ele.text.strip() for ele in hcols]
        data.append([ele for ele in hcols if ele])        
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = [ele.text.strip() for ele in row.find_all('th')]
            cols += [ele.text.strip() for ele in row.find_all('td')]
            data.append([ele for ele in cols if ele])
        fname = f"/Users/stevendungan/mvp/scrapedata/{tid}_{year}.csv"
        with open(fname, 'w') as file:
            wr = csv.writer(file)
            wr.writerows(data)

    