# import dependencies
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

team_name_1 = []

# get the html file using request
url_list = ['https://www.vlr.gg/91583/akrew-vs-100-thieves-knights-circuit-monthly-2022-april-ro16/?game=all&tab=overview','https://www.vlr.gg/91578/faze-clan-vs-zero-marksmen-black-knights-circuit-monthly-2022-april-ro16' , 'https://www.vlr.gg/91579/tsm-vs-cloud9-academy-knights-circuit-monthly-2022-april-ro16/?game=78173&tab=overview']
for url in url_list:
    html_txt = requests.get(url)
    soup = BeautifulSoup(html_txt.text, 'lxml')
    # get the match_stats
    game_stats = soup.find('div', class_="vm-stats-container")
    table_info = game_stats.find('table', class_='wf-table-inset mod-overview')

    # create a game_id variable
    game_id = []
    number_of_games = 2

    i = 1
    while i <= number_of_games:
        x = 0
        while x < 5:
            game_id.append(i)
            x+=1
        i+=1

    # score for team L
    # map to the data
    stat_game = soup.find('div', class_='vm-stats-game')
    game_header = stat_game.find('div', class_='vm-stats-game-header')
    div_team = game_header.find('div', class_='team')

    # create lists to hold the data
    score_left = []
    ct_score_left = []
    t_score_left = []
    team_left = []

    # append the values to each list
    score_l = div_team.find('div', class_='score').text
    ct_score_l = div_team.find('span', class_='mod-ct').text
    t_score_l = div_team.find('span', class_='mod-t').text
    team_l = div_team.find('div', class_='team-name').text

    # remove the weird text by using regex
    p = '\n\t*'
    p1 = '\t*'
    team_l = re.sub(p, '', team_l)
    team_l = re.sub(p1, '', team_l)

    # append the lists to have 5 of each in them so that we can paste it into the table
    i = 0
    while i<5:
        team_left.append(team_l)
        score_left.append(int(score_l))
        ct_score_left.append(int(ct_score_l))
        t_score_left.append(int(t_score_l))
        i+=1

    team_name_1.append(team_l)

match_dict = {
    'Team 1': team_name_1,
    # 'Team 2': team_name_2
}

print(match_dict)