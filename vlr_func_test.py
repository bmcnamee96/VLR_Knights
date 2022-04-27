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
import pymongo

def vlr(tourney_url):
    
    # import dependencies
    from bs4 import BeautifulSoup
    import requests
    import re
    import timeit
    
    #beginning the timer
    start = timeit.default_timer()

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

    print('Beginning URL Retrieval')
    print('------------------------')

    # get the html file using request
    html_txt = requests.get('https://www.vlr.gg/event/matches/941/knights-circuit-monthly-2022-april/?series_id=all')
    soup = BeautifulSoup(html_txt.text, 'lxml')

    try:
        # map to the correct location in the html file
        body = soup.find('body')
        div_container = body.find('div', class_='col-container')
        div_card = div_container.find_all('div', class_='wf-card')
        url_list = []

        for idx, x in enumerate(div_card):
            if idx != 0:
                # create a base_url
                base_link = []
                base_url = f'https://www.vlr.gg'
                for link in div_card[idx].find_all('a'):
                    base_link.append(link.get('href'))


                for url in base_link:
                    url_list.append(f'{base_url}{url}')
                    
    except AttributeError:
            print('There was a missing URL')

    print('------------------------')
    print(f'Found {len(url_list)} games!\n')
    
############################################################################# 

    print('Beginning Stat Retrieval')
    print('------------------------')
    
    # loop through the urls
    for idx, url in enumerate(url_list):
        
        try:
            # get the html file using request
            html_txt = requests.get(url)
            soup = BeautifulSoup(html_txt.text, 'lxml')
            game = soup.find('div', class_='vm-stats-game')
            table_info = game.find('table', class_='wf-table-inset mod-overview')
        except AttributeError:
            print(f'No game data for game {idx}')

        game_maps = len(soup.find_all('div', class_='vm-stats-game'))
    
############################################################################# 

        z=0
        for x in range(game_maps-1):
            # get all the player names and team abreviation
            body = table_info.find('tbody')
            tr = body.find_all('tr')

            # temporary variables
            a=[]
            # create lists to hold each string of information
            name_web=[]
            team_web=[]
            team_close=[]

            # map
            game_header = game.find('div', class_='vm-stats-game-header')
            div_map = game_header.find('div', class_='map')
            div_style = div_map.find('div')
            span_map = div_style.find('span').text
            # remove the weird letters
            p = '\n\t*'
            p1 = '\t*'
            span_map = re.sub(p, '', span_map)
            span_map = re.sub(p1, '', span_map)
            # remove the word PICK from the string
            p2 = 'PICK'
            map_str= re.sub(p2, '', span_map)
            # fill the list with the map names
            i = 0
            while i<10:
                game_map_player.append(map_str)
                i+=1
            game_map_match.append(map_str)
            
############################################################################# 
    
            # all stats for the map 
            y=0
            while y < 2:
                # use a while loop to access each players info and send it into the list
                x=0
                while x < len(tr):
                    trx = tr[x]
                    # name and team_abrev
                    td_name = trx.find('td', class_='mod-player')
                    div = td_name.find('div')
                    a.append(div.find('a'))
                    # stats acs, kill, death, assists
                    # acs
                    td_stat = trx.find('td', class_='mod-stat')
                    span_sq = td_stat.find('span', class_='stats-sq')
                    acs_both.append(span_sq.find('span', class_='side mod-side mod-both').get_text(strip=True))
                    acs_t.append(span_sq.find('span', class_='side mod-side mod-t').get_text(strip=True))
                    acs_ct.append(span_sq.find('span', class_='side mod-side mod-ct').get_text(strip=True))
                    # kills
                    td_stat = trx.find('td', class_='mod-stat mod-vlr-kills')
                    span_sq = td_stat.find('span', class_='stats-sq')
                    kill_both.append(span_sq.find('span', class_='side mod-side mod-both').get_text(strip=True))
                    kill_t.append(span_sq.find('span', class_='side mod-side mod-t').get_text(strip=True))
                    kill_ct.append(span_sq.find('span', class_='side mod-side mod-ct').get_text(strip=True))
                    # deaths
                    td_stat = trx.find('td', class_='mod-stat mod-vlr-deaths')
                    span_sq = td_stat.find('span', class_='stats-sq')
                    death_both.append(span_sq.find('span', class_='side mod-both').get_text(strip=True))
                    death_t.append(span_sq.find('span', class_='side mod-t').get_text(strip=True))
                    death_ct.append(span_sq.find('span', class_='side mod-ct').get_text(strip=True))
                    # assists
                    td_stat = trx.find('td', class_='mod-stat mod-vlr-assists')
                    span_sq = td_stat.find('span', class_='stats-sq')
                    assist_both.append(span_sq.find('span', class_='side mod-both').get_text(strip=True))
                    assist_t.append(span_sq.find('span', class_='side mod-t').get_text(strip=True))
                    assist_ct.append(span_sq.find('span', class_='side mod-ct').get_text(strip=True))

                    x+=1

                # go to the next 'table' to find the stats of the other team
                if y == 0:
                    table_info = table_info.find_next('table', class_='wf-table-inset mod-overview')
                    body = table_info.find('tbody')
                    tr = body.find_all('tr')
                    
############################################################################# 
    
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

                # clear temporary variables
                a = []
                name_web=[]
                team_web=[]
                team_close = []

                y+=1

                # mapping to the next maps
                if z == 0:
                    # map 2
                    # need to find_next because 'all' is the 2nd tab
                    game = game.find_next('div', class_='vm-stats-game')
                    game = game.find_next('div', class_='vm-stats-game')
                elif z == 1:
                    # map 3
                    game = game.find_next('div', class_='vm-stats-game')

                z+=x
############################################################################# 
    # finding the game id based on the length of the data we have
    
    i=0
    while i < len(team_abrev)/10:
        game_id_match.append(i)
        z=0
        while z < 10:
            game_id_player.append(i)
            z+=1
        i+=1
        
    print('------------------------')
    # ending the timer
    end = timeit.default_timer()
    time_sec = end - start
    time_sec = "{:.2f}".format(time_sec)
    print(f'Stats retrieved in {time_sec} seconds')
    
    return


vlr('https://www.vlr.gg/event/matches/941/knights-circuit-monthly-2022-april/?series_id=all')

#############################################################################

# matches_dict = {
    # 'Game ID': game_id_match, 
#     'Team 1': team_left,
#     'Score: Team 1': score_left,
#     'Team 2': team_right,
#     'Score: Team 2': score_right,
    # 'Map': game_map_match,
#     # 'Team Map Pick':
#     'Score CT: Team 1': ct_score_left,
#     'Score T: Team 1': t_score_left,
#     'Score CT: Team 2': ct_score_right,
#     'Score T: Team 2': t_score_right,
#     # 'Match Length':
#}

# matches_df = pd.DataFrame(matches_dict)

player_stat_dict = {
    'game_id': game_id_player,
    'player_name': name,
    'team_abrev': team_abrev,
    'map': game_map_player,
    'acs_both': acs_both,
    'acs_t': acs_t,
    'acs_ct': acs_ct,
    'kill_both': kill_both,
    'kill_t': kill_t,
    'kill_ct': kill_ct,
    'death_both': death_both,
    'death_t': death_t,
    'death_ct': death_ct,
    'assist_both': assist_both,
    'assist_t': assist_t,
    'assist_ct': assist_ct
    # 'adr':
    # 'first_kills':
    # 'first_deaths':
}

# create a df from the dictionary
player_game_df = pd.DataFrame(player_stat_dict)
player_game_df = player_game_df.replace(r'', np.nan, regex=True)

# change the data type from object to float
player_game_df['acs_both'] = pd.to_numeric(player_game_df['acs_both'])
player_game_df['acs_t'] = pd.to_numeric(player_game_df['acs_t'])
player_game_df['acs_ct'] = pd.to_numeric(player_game_df['acs_ct'])
player_game_df['kill_both'] = pd.to_numeric(player_game_df['kill_both'])
player_game_df['kill_t'] = pd.to_numeric(player_game_df['kill_t'])
player_game_df['kill_ct'] = pd.to_numeric(player_game_df['kill_ct'])
player_game_df['death_both'] = pd.to_numeric(player_game_df['death_both'])
player_game_df['death_t'] = pd.to_numeric(player_game_df['death_t'])
player_game_df['death_ct'] = pd.to_numeric(player_game_df['death_ct'])
player_game_df['assist_both'] = pd.to_numeric(player_game_df['assist_both'])
player_game_df['assist_t'] = pd.to_numeric(player_game_df['assist_t'])
player_game_df['assist_ct'] = pd.to_numeric(player_game_df['assist_ct'])

# drop any rows with null values
player_game_df = player_game_df.dropna()

print(player_game_df.head(10))
print(player_game_df.tail(10))






#############################################################################
# fill the db with the 

# from sqlalchemy import create_engine
# import psycopg2
# import time

# db_password = 'postgres'

# db_string = f'postgresql://postgres:{db_password}@127.0.0.1:5432/vlr_knights'
# engine = create_engine(db_string)
    
# player_game_df.to_sql(name='vlr_knights', con=engine, if_exists='replace')
