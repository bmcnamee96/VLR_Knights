# import dependencies
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import tabulate

base_url = 'https://www.vlr.gg/event/matches/941/knights-circuit-monthly-2022-april/?series_id=all'
# get the html file using request
html_txt = requests.get(base_url)
soup = BeautifulSoup(html_txt.text, 'lxml')

# map to the correct location in the htm file
body = soup.find('body')
div_container = body.find('div', class_='col-container')
div_card = div_container.find('div', class_='wf-card')
div_card = div_card.find_next('div', class_='wf-card')

# create a base_url
base_link = []
base_url = f'https://www.vlr.gg'
for link in div_card.find_all('a'):
    base_link.append(link.get('href'))

# create a url list to hold all of the urls to loop through
url_list = []
for url in base_link:
    url_list.append(f'{base_url}{url}')

# final variables
# variables to hold the player information
name = []
team_abrev = []
# create lists to hold the data
acs_both = []
acs_t = []
acs_ct = []
kill_both = []
kill_t = []
kill_ct = []
death_both = []
death_t = []
death_ct = []
assist_both = []
assist_t = []
assist_ct = []
# create a game_id variable
game_id_match = []
game_id_player = []
# find the game_id    
list_num_map = []
url_num = 0

# create all of our variables before starting the loop
for url in url_list:

    try:
        # get the html file using request
        html_txt = requests.get(url)
        soup = BeautifulSoup(html_txt.text, 'lxml')
        # get the match_stats
        game_stats = soup.find('div', class_="vm-stats-container")

        # for baseline game
        game = soup.find('div', class_='vm-stats-game')
        table_info = game.find('table', class_='wf-table-inset mod-overview')
    except AttributeError:
        print('No Game Data')
    # temporary variables
    # create a variable to hold our webscraped info
    a = []
    # create lists to hold each string of information
    name_web=[]
    team_web=[]
    team_close = []

    game_maps = len(soup.find_all('div', class_='vm-stats-game'))

#############################################################################  
    
    # looping through all 3 maps to find the player names in all 3 maps
    z=0
    while z < game_maps - 1:
        # get all the player names and team abreviation team 1
        table_info = game.find('table', class_='wf-table-inset mod-overview')
        body = table_info.find('tbody')
        tr = body.find_all('tr')

#############################################################################    
    # Player Name and Team Abbreviation  
        y=0
        while y < 2:
            # map to the correct location
            body = table_info.find('tbody')
            tr = body.find_all('tr')

                # use a while loop to access each players info and send it into the list
            x=0
            while x < len(tr):
                trx = tr[x]
                td_name = trx.find('td', class_='mod-player')
                div = td_name.find('div')
                a.append(div.find('a'))
                x+=1

            # use a while loop to find the info that we need and put it into the lists
            i=0
            while i < len(a):
                ai = a[i]
                name_web.append(ai.find('div', class_='text-of').text)
                team_web.append(ai.find('div', class_='ge-text-light').text)
                i+=1

            # use regex to fix the names
            p = '\n\t*'
            p1 = '\t*'
            for n in name_web:
                name.append(re.sub(p, '', n))

            for n in team_web:
                team_close.append(re.sub(p, '', n))
            for b in team_close:
                team_abrev.append(re.sub(p1, '', b))

            if y == 0:
                table_info = game.find('table', class_='wf-table-inset mod-overview')
                table_info = table_info.find_next('table', class_='wf-table-inset mod-overview')

            # clear temporary variables
            a = []
            name_web=[]
            team_web=[]
            team_close = []

            y+=1

############################################################################# 
    # ACS, ACS_t, ACS_ct
        y=0
        table_info = game.find('table', class_='wf-table-inset mod-overview')
        while y < 2:
            # mapping to the correct location for all player for acs
            body = table_info.find('tbody')
            tr = body.find_all('tr')
            # use a while loop to get to the information for each player and add it into our lists

            x=0
            while x < len(tr):
                trx = tr[x]
                td_stat = trx.find('td', class_='mod-stat')
                span_sq = td_stat.find('span', class_='stats-sq')
                acs_both.append(span_sq.find('span', class_='side mod-side mod-both').get_text(strip=True))
                acs_t.append(span_sq.find('span', class_='side mod-side mod-t').get_text(strip=True))
                acs_ct.append(span_sq.find('span', class_='side mod-side mod-ct').get_text(strip=True))
                x+=1

            if y == 0:
                    table_info = table_info.find_next('table', class_='wf-table-inset mod-overview')

            y+=1

#############################################################################
    # Kills, Kills_t, Kills_ct  
        y=0
        table_info = game.find('table', class_='wf-table-inset mod-overview')
        while y < 2:
            # mapping to the correct location for all player for acs
            body = table_info.find('tbody')
            tr = body.find_all('tr')
            # use a while loop to get to the information for each player and add it into our lists

            x=0
            while x < len(tr):
                trx = tr[x]
                td_stat = trx.find('td', class_='mod-stat mod-vlr-kills')
                span_sq = td_stat.find('span', class_='stats-sq')
                kill_both.append(span_sq.find('span', class_='side mod-side mod-both').get_text(strip=True))
                kill_t.append(span_sq.find('span', class_='side mod-side mod-t').get_text(strip=True))
                kill_ct.append(span_sq.find('span', class_='side mod-side mod-ct').get_text(strip=True))
                x+=1

            if y == 0:
                    table_info = table_info.find_next('table', class_='wf-table-inset mod-overview')

            y+=1

#############################################################################
    # Deaths, Deaths_t, Deaths_ct
        y=0
        table_info = game.find('table', class_='wf-table-inset mod-overview')
        while y < 2:
            # mapping to the correct location for all player for deaths
            body = table_info.find('tbody')
            tr = body.find_all('tr')
            # use a while loop to get to the information for each player and add it into our list

            x=0
            while x < len(tr):
                trx = tr[x]
                td_stat = trx.find('td', class_='mod-stat mod-vlr-deaths')
                span_sq = td_stat.find('span', class_='stats-sq')
                death_both.append(span_sq.find('span', class_='side mod-both').get_text(strip=True))
                death_t.append(span_sq.find('span', class_='side mod-t').get_text(strip=True))
                death_ct.append(span_sq.find('span', class_='side mod-ct').get_text(strip=True))
                x+=1

            if y == 0:
                table_info = table_info.find_next('table', class_='wf-table-inset mod-overview')

            y+=1

#############################################################################
    # Assists, Assists_t, Assists_ct
        y=0
        table_info = game.find('table', class_='wf-table-inset mod-overview')
        while y < 2:
            # mapping to the correct location for all player for deaths
            body = table_info.find('tbody')
            tr = body.find_all('tr')
            # use a while loop to get to the information for each player and add it into our lists
            x=0
            while x < len(tr):
                trx = tr[x]
                td_stat = trx.find('td', class_='mod-stat mod-vlr-assists')
                span_sq = td_stat.find('span', class_='stats-sq')
                assist_both.append(span_sq.find('span', class_='side mod-both').get_text(strip=True))
                assist_t.append(span_sq.find('span', class_='side mod-t').get_text(strip=True))
                assist_ct.append(span_sq.find('span', class_='side mod-ct').get_text(strip=True))
                x+=1

            if y == 0:
                    table_info = table_info.find_next('table', class_='wf-table-inset mod-overview')

            y+=1

#############################################################################

        if z == 0:
            # map 2
            game = soup.find('div', class_='vm-stats-game')
            game = game.find_next('div', class_='vm-stats-game')
            game = game.find_next('div', class_='vm-stats-game')
        elif z == 1:
            game = game.find_next('div', class_='vm-stats-game')

        z+=1
        
#############################################################################
# Game ID

i=0
while i < len(team_abrev)/10:
    game_id_match.append(i)
    z=0
    while z < 10:
        game_id_player.append(i)
        z+=1
    i+=1


#############################################################################


player_stat_dict = {
    'Game ID': game_id_player,
    'Player Name': name,
    'Team Abbreviation': team_abrev,
    # 'Map': game_map_player,
    'ACS Total': acs_both,
    'ACS Attack': acs_t,
    'ACS Defense': acs_ct,
    'Kill Total': kill_both,
    'Kill Attack': kill_t,
    'Kill Defense': kill_ct,
    'Death Total': death_both,
    'Death Attack': death_t,
    'Death Defense': death_ct,
    'Assist Total': assist_both,
    'Assist Attack': assist_t,
    'Assist Defense': assist_ct
    # 'ADR':
    # 'First Kills':
    # 'First Deaths':
}

# create a df from the dictionary
player_game_df = pd.DataFrame(player_stat_dict)
player_game_df = player_game_df.replace(r'', np.nan, regex=True)

# change the data type from object to float
player_game_df['ACS Total'] = pd.to_numeric(player_game_df['ACS Total'])
player_game_df['ACS Attack'] = pd.to_numeric(player_game_df['ACS Attack'])
player_game_df['ACS Defense'] = pd.to_numeric(player_game_df['ACS Defense'])
player_game_df['Kill Total'] = pd.to_numeric(player_game_df['Kill Total'])
player_game_df['Kill Attack'] = pd.to_numeric(player_game_df['Kill Attack'])
player_game_df['Kill Defense'] = pd.to_numeric(player_game_df['Kill Defense'])
player_game_df['Death Total'] = pd.to_numeric(player_game_df['Death Total'])
player_game_df['Death Attack'] = pd.to_numeric(player_game_df['Death Attack'])
player_game_df['Death Defense'] = pd.to_numeric(player_game_df['Death Defense'])
player_game_df['Assist Total'] = pd.to_numeric(player_game_df['Assist Total'])
player_game_df['Assist Attack'] = pd.to_numeric(player_game_df['Assist Attack'])
player_game_df['Assist Defense'] = pd.to_numeric(player_game_df['Assist Defense'])

# drop any rows with null values
player_game_df = player_game_df.dropna()