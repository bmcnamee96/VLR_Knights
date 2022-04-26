# import dependencies
from enum import unique
from operator import contains
from time import time
from bs4 import BeautifulSoup
from certifi import contents
import requests
import re
import pandas as pd
import numpy as np
import timeit

# using a for loop, loop through all of the urls
# each iteration of the for loop goes to the next map
def vlr(tourney_url):

    # import dependencies
    from bs4 import BeautifulSoup
    import requests
    import re
    import pandas as pd
    import numpy as np

    # create variables for player stats
    # make them global so that they can be accessed outside of the func
    global name
    name = []
    global team_abrev
    team_abrev = []
    global acs_both
    acs_both = []
    global acs_t
    acs_t = []
    global acs_ct
    acs_ct = []
    global kill_both
    kill_both = []
    global kill_t
    kill_t = []
    global kill_ct
    kill_ct = []
    global death_both
    death_both = []
    global death_t
    death_t = []
    global death_ct
    death_ct = []
    global assist_both
    assist_both = []
    global assist_t
    assist_t = []
    global assist_ct
    assist_ct = []
    global game_id_player
    game_id_player = []
    global game_map_player
    game_map_player = []

    # create variables for match stats
    # make them global so that they can be accessed outside of the func
    global game_id_match
    game_id_match = []
    global game_map_match
    game_map_match = []
    
    ############################################################################# 
    
    # get the html file using request
    html_txt = requests.get(tourney_url)
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

    url_list = []
    for url in base_link:
        url_list.append(f'{base_url}{url}')

    for idx, url in enumerate(url_list):

        try:
            # get the html file using request
            html_txt = requests.get(url)
            soup = BeautifulSoup(html_txt.text, 'lxml')
            # get the match_stats
            # game_stats = soup.find('div', class_="vm-stats-container")

            # for baseline game
            game = soup.find('div', class_='vm-stats-game')
            table_info = game.find('table', class_='wf-table-inset mod-overview')
        except AttributeError:
            print(f'No game data for game {idx}')

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
        for x in range(game_maps - 1):
            # get all the player names and team abreviation
            table_info = game.find('table', class_='wf-table-inset mod-overview')
            body = table_info.find('tbody')
            tr = body.find_all('tr')

    ############################################################################# 
        # get the map
            # map to the area we need
            stat_game = soup.find('div', class_='vm-stats-game')
            game_header = stat_game.find('div', class_='vm-stats-game-header')
            div_map = game_header.find('div', class_='map')
            div_style = div_map.find('div')
            # get the text needed
            span_map = div_style.find('span').text

            # remove the weird letters
            p = '\n\t*'
            p1 = '\t*'
            span_map = re.sub(p, '', span_map)
            span_map = re.sub(p1, '', span_map)

            # remove the word PICK from the string
            i = []
            for x in span_map:
                if x != 'P' or x != 'I' or x != 'C' or x != 'K':
                    i.append(x)

            # append the map list so that it is equal length 
            map_str = ''.join(i)

            i = 0
            while i<10:
                game_map_player.append(map_str)
                i+=1
            game_map_match.append(map_str)

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

            z+=x
            
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
    
    return


start = timeit.default_timer()
vlr('https://www.vlr.gg/event/matches/941/knights-circuit-monthly-2022-april/?series_id=all')
end = timeit.default_timer()

print(end-start)
#############################################################################

matches_dict = {
    # 'Game ID': game_id_match, 
#     'Team 1': team_left,
#     'Score: Team 1': score_left,
#     'Team 2': team_right,
#     'Score: Team 2': score_right,
    'Map': game_map_match,
#     # 'Team Map Pick':
#     'Score CT: Team 1': ct_score_left,
#     'Score T: Team 1': t_score_left,
#     'Score CT: Team 2': ct_score_right,
#     'Score T: Team 2': t_score_right,
#     # 'Match Length':
}

matches_df = pd.DataFrame(matches_dict)

player_stat_dict = {
    'Game ID': game_id_player,
    'Player Name': name,
    'Team Abbreviation': team_abrev,
    'Map': game_map_player,
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

print(player_game_df.head(50))
# print(player_game_df)
# print(matches_df)
#############################################################################
# fill the db with the 

# from sqlalchemy import create_engine
# import psycopg2
# import time

# db_password = 'postgres'

# db_string = f'postgresql://postgres:{db_password}@127.0.0.1:5432/vlr_knights'
# engine = create_engine(db_string)
    
# player_game_df.to_sql(name='vlr_knights', con=engine, if_exists='replace')
