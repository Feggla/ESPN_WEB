from flask import Flask, render_template, url_for, redirect, request, session, jsonify
from espn_api.basketball import League
import pandas as pd
import time
from Team_web import Teams
import re
from dotenv import load_dotenv
import os
from rankings import check_rankings
from data import update_db_rankings
from testing import get_rankings, process_rankings
from matchweek import assign_matchweek
from depen import get_db_connection
from flask_cors import CORS





load_dotenv()
leagues = {
    'aleague': {
        'id': 16786,
        's2': 'AEC0gxRVe7LwBwGt2A%2B4a2kf6Vauml1tfM%2BcReJAljodq7NlOX5VxydaVeqQPYcRpokw2TeZcRFlJK%2B99R1QzVCo9mArW79anJC%2Fca%2F8LzbKMj4xcJJ%2BLTyxwO%2FYxeQczRH41cDYec2T%2F9Z0CJpA8Aa170MPGCDSQkXtDYmAQa%2Bud8X5ZYAIWtTjLSVcQIUw2hJTADna%2Fh74tK4HHFTJFDvElNjYXXACwkgGyNUpFa7uHhxyzvssypqRtx9BglTy2S41Beg9zPFaws60Xi1cZHuFNHKNKcgtKXlrpehwPRpD8U9H05BLfGxBfOPsceP8CQI%3D,',
        'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    },
    'bleague': {
        'id': 84279,
        's2': 'AEC0gxRVe7LwBwGt2A%2B4a2kf6Vauml1tfM%2BcReJAljodq7NlOX5VxydaVeqQPYcRpokw2TeZcRFlJK%2B99R1QzVCo9mArW79anJC%2Fca%2F8LzbKMj4xcJJ%2BLTyxwO%2FYxeQczRH41cDYec2T%2F9Z0CJpA8Aa170MPGCDSQkXtDYmAQa%2Bud8X5ZYAIWtTjLSVcQIUw2hJTADna%2Fh74tK4HHFTJFDvElNjYXXACwkgGyNUpFa7uHhxyzvssypqRtx9BglTy2S41Beg9zPFaws60Xi1cZHuFNHKNKcgtKXlrpehwPRpD8U9H05BLfGxBfOPsceP8CQI%3D',
        'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    },
    'cleague' : {
        'id': 13466,
        's2': 'AEBdl1ip92PTF6YAfxtjHSpy3bEkny6dJwBmSHq4F8k9y5rnMQMbQ4%2BqZx5Ojj%2BMHExw0z4vXCQQ9tCZOKAtuKcv439NtsOZZTd0eMS0CFHSx%2BuASDdAa%2B99H4UVWrdATWEK9IrGjX0gTQE08hoKdOvS0rC0t9z7SGvt3uRIzZtJu2XiS2bPPOik7nak1tE8D0iQI5jXYukzmxf7IngRtzmVq2AuyZeVxqA%2FpVhZ2aTz%2Fxd0HQ2D%2BiUkzSNr%2BJbvlF68zvLMDsXxW4ROrozGNCKz335azpmA23it%2F93cVLBwEgM94F3qW3WBKNVrowHkWg4%3D',
        'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    },
    'dleague': {
        'id': 17245,
        's2': 'AEC0gxRVe7LwBwGt2A%2B4a2kf6Vauml1tfM%2BcReJAljodq7NlOX5VxydaVeqQPYcRpokw2TeZcRFlJK%2B99R1QzVCo9mArW79anJC%2Fca%2F8LzbKMj4xcJJ%2BLTyxwO%2FYxeQczRH41cDYec2T%2F9Z0CJpA8Aa170MPGCDSQkXtDYmAQa%2Bud8X5ZYAIWtTjLSVcQIUw2hJTADna%2Fh74tK4HHFTJFDvElNjYXXACwkgGyNUpFa7uHhxyzvssypqRtx9BglTy2S41Beg9zPFaws60Xi1cZHuFNHKNKcgtKXlrpehwPRpD8U9H05BLfGxBfOPsceP8CQI%3D',
        'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    },
    'eleague': {
        'id': 69134545,
        's2': 'AEC0gxRVe7LwBwGt2A%2B4a2kf6Vauml1tfM%2BcReJAljodq7NlOX5VxydaVeqQPYcRpokw2TeZcRFlJK%2B99R1QzVCo9mArW79anJC%2Fca%2F8LzbKMj4xcJJ%2BLTyxwO%2FYxeQczRH41cDYec2T%2F9Z0CJpA8Aa170MPGCDSQkXtDYmAQa%2Bud8X5ZYAIWtTjLSVcQIUw2hJTADna%2Fh74tK4HHFTJFDvElNjYXXACwkgGyNUpFa7uHhxyzvssypqRtx9BglTy2S41Beg9zPFaws60Xi1cZHuFNHKNKcgtKXlrpehwPRpD8U9H05BLfGxBfOPsceP8CQI%3D',
        'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    },
    'fleague': {
        'id': 44307788,
        's2': 'AEC0gxRVe7LwBwGt2A%2B4a2kf6Vauml1tfM%2BcReJAljodq7NlOX5VxydaVeqQPYcRpokw2TeZcRFlJK%2B99R1QzVCo9mArW79anJC%2Fca%2F8LzbKMj4xcJJ%2BLTyxwO%2FYxeQczRH41cDYec2T%2F9Z0CJpA8Aa170MPGCDSQkXtDYmAQa%2Bud8X5ZYAIWtTjLSVcQIUw2hJTADna%2Fh74tK4HHFTJFDvElNjYXXACwkgGyNUpFa7uHhxyzvssypqRtx9BglTy2S41Beg9zPFaws60Xi1cZHuFNHKNKcgtKXlrpehwPRpD8U9H05BLfGxBfOPsceP8CQI%3D',
        'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    },
    'gleague': {
        'id': 25245250,
        's2': 'AEC0gxRVe7LwBwGt2A%2B4a2kf6Vauml1tfM%2BcReJAljodq7NlOX5VxydaVeqQPYcRpokw2TeZcRFlJK%2B99R1QzVCo9mArW79anJC%2Fca%2F8LzbKMj4xcJJ%2BLTyxwO%2FYxeQczRH41cDYec2T%2F9Z0CJpA8Aa170MPGCDSQkXtDYmAQa%2Bud8X5ZYAIWtTjLSVcQIUw2hJTADna%2Fh74tK4HHFTJFDvElNjYXXACwkgGyNUpFa7uHhxyzvssypqRtx9BglTy2S41Beg9zPFaws60Xi1cZHuFNHKNKcgtKXlrpehwPRpD8U9H05BLfGxBfOPsceP8CQI%3D',
        'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    },
    'hleague': {
        'id': 130855514,
        's2': 'AEC0gxRVe7LwBwGt2A%2B4a2kf6Vauml1tfM%2BcReJAljodq7NlOX5VxydaVeqQPYcRpokw2TeZcRFlJK%2B99R1QzVCo9mArW79anJC%2Fca%2F8LzbKMj4xcJJ%2BLTyxwO%2FYxeQczRH41cDYec2T%2F9Z0CJpA8Aa170MPGCDSQkXtDYmAQa%2Bud8X5ZYAIWtTjLSVcQIUw2hJTADna%2Fh74tK4HHFTJFDvElNjYXXACwkgGyNUpFa7uHhxyzvssypqRtx9BglTy2S41Beg9zPFaws60Xi1cZHuFNHKNKcgtKXlrpehwPRpD8U9H05BLfGxBfOPsceP8CQI%3D',
        'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    },
    'ileague': {
        'id': 297414126,
        's2': 'AEC0gxRVe7LwBwGt2A%2B4a2kf6Vauml1tfM%2BcReJAljodq7NlOX5VxydaVeqQPYcRpokw2TeZcRFlJK%2B99R1QzVCo9mArW79anJC%2Fca%2F8LzbKMj4xcJJ%2BLTyxwO%2FYxeQczRH41cDYec2T%2F9Z0CJpA8Aa170MPGCDSQkXtDYmAQa%2Bud8X5ZYAIWtTjLSVcQIUw2hJTADna%2Fh74tK4HHFTJFDvElNjYXXACwkgGyNUpFa7uHhxyzvssypqRtx9BglTy2S41Beg9zPFaws60Xi1cZHuFNHKNKcgtKXlrpehwPRpD8U9H05BLfGxBfOPsceP8CQI%3D',
        'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    },
    'jleague': {
        'id': 1888308229,
        's2': 'AEC0gxRVe7LwBwGt2A%2B4a2kf6Vauml1tfM%2BcReJAljodq7NlOX5VxydaVeqQPYcRpokw2TeZcRFlJK%2B99R1QzVCo9mArW79anJC%2Fca%2F8LzbKMj4xcJJ%2BLTyxwO%2FYxeQczRH41cDYec2T%2F9Z0CJpA8Aa170MPGCDSQkXtDYmAQa%2Bud8X5ZYAIWtTjLSVcQIUw2hJTADna%2Fh74tK4HHFTJFDvElNjYXXACwkgGyNUpFa7uHhxyzvssypqRtx9BglTy2S41Beg9zPFaws60Xi1cZHuFNHKNKcgtKXlrpehwPRpD8U9H05BLfGxBfOPsceP8CQI%3D',
        'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    },
    'kleague': {
        'id': 131200104,
        's2': 'AEC0gxRVe7LwBwGt2A%2B4a2kf6Vauml1tfM%2BcReJAljodq7NlOX5VxydaVeqQPYcRpokw2TeZcRFlJK%2B99R1QzVCo9mArW79anJC%2Fca%2F8LzbKMj4xcJJ%2BLTyxwO%2FYxeQczRH41cDYec2T%2F9Z0CJpA8Aa170MPGCDSQkXtDYmAQa%2Bud8X5ZYAIWtTjLSVcQIUw2hJTADna%2Fh74tK4HHFTJFDvElNjYXXACwkgGyNUpFa7uHhxyzvssypqRtx9BglTy2S41Beg9zPFaws60Xi1cZHuFNHKNKcgtKXlrpehwPRpD8U9H05BLfGxBfOPsceP8CQI%3D',
        'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    },
    'lleague': {
        'id': 366757782,
        's2': 'AEC0gxRVe7LwBwGt2A%2B4a2kf6Vauml1tfM%2BcReJAljodq7NlOX5VxydaVeqQPYcRpokw2TeZcRFlJK%2B99R1QzVCo9mArW79anJC%2Fca%2F8LzbKMj4xcJJ%2BLTyxwO%2FYxeQczRH41cDYec2T%2F9Z0CJpA8Aa170MPGCDSQkXtDYmAQa%2Bud8X5ZYAIWtTjLSVcQIUw2hJTADna%2Fh74tK4HHFTJFDvElNjYXXACwkgGyNUpFa7uHhxyzvssypqRtx9BglTy2S41Beg9zPFaws60Xi1cZHuFNHKNKcgtKXlrpehwPRpD8U9H05BLfGxBfOPsceP8CQI%3D',
        'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    },
    'mleague': {
    'id': 1398223150,
    's2': 'AECq2PGl8JUq15avsstcUVvVa0Das5InBxnTGVGoTnXYpifyw6aNwjcJshQaTEKmhnyTkcrXm%2F1JKIPfg7rqdFXlozIM07ci0JBXvH35lPjWjOs%2FIbJcgvRZCgDpsb49tiz%2Fcl0Fk0B10ACgeXTI8tW11xkNdoqIHvd0j8p86wHQoApn12cHBe%2B9sr5H%2FOPE%2BoKomBegwA%2BIVe0Rc0KoTi0iCITtOZ1dyqzyATcaFrNtUs3f%2B3RRfMJrE9RvU8Af6NtbziCg%2FbG5jfG18FduftldLczSwoye9dKwA3AkZdKE%2F1VwocvLjDv2sHdLPmaOfpQ%3D',
    'swid': '{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}'
    }
}
overall_list = []
current_matchweek = assign_matchweek()
# current_matchweek = 17

def pull(matchup_period, leagues):
    overall_list.clear()
    scoreboards_dic = {}
    for association in leagues:
        team_matchups = []
        score_list = []
        league = League(league_id=leagues[association]['id'], year=2024, espn_s2=leagues[association]['s2'], swid=leagues[association]['swid'])
        scoreboard = league.box_scores(matchup_period=matchup_period, scoring_period=1, matchup_total=True)
        scoreboards_dic[association] = scoreboard
        score = league.scoreboard(matchupPeriod=matchup_period)

        for items in scoreboard:
            team_matchups.append([items.home_team, items.away_team])
        for games in team_matchups:
            games[0] = Teams(mw=matchup_period, player=team_matchups.index(games), place="home", league=league,
                             scoreboard=scoreboard, score=score)
            games[1] = Teams(mw=matchup_period, player=team_matchups.index(games), place="away", league=league,
                             scoreboard=scoreboard, score=score)
            games[0].league = association[0].upper()
            games[1].league = association[0].upper()
            overall_list.append(games[0])
            overall_list.append(games[1])
            score_list.append(games[0])
            score_list.append(games[1])

new_matchups = []

# def add_to_rankings(clean_list):
#     rankings = check_rankings(clean_list)
#     for team, scores in rankings.items():
#         rankings[team] = [scores[0] + 0.5 * scores[1], scores[2]]
#     sorted_rankings = dict(sorted(rankings.items(), key=lambda item: item[1][0], reverse=True))
#     data = [(team, *scores) for team, scores in sorted_rankings.items()]
#     rank_df = pd.DataFrame(data, columns=['Team', 'Matchups Score', 'League'])
#     min_score = float(rank_df['Matchups Score'].min())
#     max_score = float(rank_df['Matchups Score'].max())
#     def calculate_colors(score):
#             if max_score == min_score:
#                 return 'rgb(255, 255, 255)'
#             red = 255 - int((score - min_score) / (max_score - min_score) * 255)
#             green = int((score - min_score) / (max_score - min_score) * 200)
#             return f'rgb({red},{green},0)'

#     rank_df['Color'] = rank_df['Matchups Score'].apply(calculate_colors)
#     rank_df["Week"] = current_matchweek

#     rank_data = rank_df.to_dict(orient='records')
#     rank_df.to_csv("week_1_data.csv")
    # update_db_rankings(rank_df)

def update(matchweek, league):
    global clean_list
    clean_list = []
    try:
        pull(matchweek, league)    
    except AttributeError:
        matchweek = matchweek-1
        pull(matchweek, league)
    for team in overall_list:
        team.name = str(team.name).replace("Team(", "").replace(")", "").strip()
        clean_list.append(team)

    clean_list = sorted(clean_list, key=lambda team: team.name)
    # add_to_rankings(clean_list)


update(current_matchweek, leagues)

# rankings = check_rankings(clean_list)
# for team, scores in rankings.items():
#     rankings[team] = [scores[0] + 0.5 * scores[1], scores[2]]
# sorted_rankings = dict(sorted(rankings.items(), key=lambda item: item[1][0], reverse=True))
# data = [(team, *scores) for team, scores in sorted_rankings.items()]
# rank_df = pd.DataFrame(data, columns=['Team', 'Matchups Score', 'League'])
# min_score = float(rank_df['Matchups Score'].min())
# max_score = float(rank_df['Matchups Score'].max())
# def calculate_colors(score):
#         if max_score == min_score:
#             return 'rgb(255, 255, 255)'
#         red = 255 - int((score - min_score) / (max_score - min_score) * 255)
#         green = int((score - min_score) / (max_score - min_score) * 200)
#         return f'rgb({red},{green},0)'

# rank_df['Color'] = rank_df['Matchups Score'].apply(calculate_colors)
# rank_df["Week"] = current_matchweek
# rank_data = rank_df.to_dict(orient='records')

def clean_names(team_list):
    for obj in team_list:
        obj.name = re.sub(' +', ' ', obj.name)

clean_names(clean_list)

outliers = []
matchup_dic = {}

df = pd.read_excel("./Knockout_Round_9.xlsx", sheet_name='Sheet1', engine='openpyxl', header=None)
pairings = df[1].dropna().tolist()
league_letters = df[0].dropna().tolist()
pairs = [(pairings[i], pairings[i+1]) for i in range(0, len(pairings), 2)]
team_entries = df.dropna(subset=[1, 2])
team_dict = {int(id): name for name, id in zip(team_entries[1], team_entries[2])}
team_items = list(team_dict.items())
pairings_list = [{team_items[i][0]: team_items[i][1], team_items[i+1][0]: team_items[i+1][1]}
                 for i in range(0, len(team_items) - 1, 2)]
round_1_matchups = []
for pair in pairs:
    team1 = pair[0]
    team2 = pair[1]
    round_1_matchups.append([team1, team2])

sorted_objects = sorted(clean_list, key=lambda obj: obj.name.lower())

id = 1


for item in sorted_objects:
    item.id = id
    id += 1

obj_list = []

new_clean_list = clean_list

for matchups in pairings_list:
    ids = list(matchups.keys())
    team1_id = ids[0]
    team2_id = ids[1]
    battle = []
    for objects in sorted_objects:
        if team1_id == objects.id:
            battle.append(objects) 
        elif team2_id == objects.id:
            battle.append(objects)
    obj_list.append(battle)

result_list = []

def check_scores(cat):
    if cat == "turnovers":
        if getattr(matchups[0], cat) > getattr(matchups[1], cat):
            matchup[matchups[1].name] += 1
        if getattr(matchups[1], cat) > getattr(matchups[0], cat):
            matchup[matchups[0].name] += 1
        if getattr(matchups[0], cat) == getattr(matchups[1], cat):
            matchup["draw"] += 1
    if cat != "turnovers":
        if getattr(matchups[0], cat) > getattr(matchups[1], cat):
            matchup[matchups[0].name] += 1
        if getattr(matchups[1], cat) > getattr(matchups[0], cat):
            matchup[matchups[1].name] += 1
        if getattr(matchups[0], cat) == getattr(matchups[1], cat):
            matchup["draw"] +=1

data_list = []

for matchups in obj_list:
    matchup = {matchups[0].name: 0,
                matchups[1].name: 0, 
                "draw" : 0
                }
    check_scores('points')
    check_scores('blocks')
    check_scores('steals')
    check_scores('assists')
    check_scores('rebounds')
    check_scores('turnovers')
    check_scores('fg')
    check_scores('ft')
    check_scores('threes')
    check_scores('three_percent')
    check_scores('td')
    
    if matchup[matchups[0].name] > matchup[matchups[1].name]:
        winner = matchups[0].name
        loser = matchups[1].name
    if matchup[matchups[1].name] > matchup[matchups[0].name]:
        winner = matchups[1].name
        loser = matchups[0].name
    if matchup[matchups[0].name] == matchup[matchups[1].name]:
        check_scores("ft")
        if matchup[matchups[0].name] > matchup[matchups[1].name]:
            winner = matchups[0].name
            loser = matchups[1].name
        if matchup[matchups[1].name] > matchup[matchups[0].name]:
            winner = matchups[1].name
            loser = matchups[0].name
        if matchup[matchups[0].name] == matchup[matchups[1].name]:
            winner = "Not Determined"
            loser = "Not Determined"
    result_list.append({
        matchups[0].name:matchup[matchups[0].name], 
        matchups[1].name: matchup[matchups[1].name],
        "Drawn": matchup['draw'],
        "Winning Team": winner,
        "Losing Team": loser
        })
    data_list.append([matchups[0].name, matchup[matchups[0].name], matchups[1].name, matchup[matchups[1].name], matchup['draw'], winner])

restructured_list = []

paired_letters = [league_letters[i:i + 2] for i in range(0, len(league_letters), 2)]
    

for result in result_list:
    # Get team names and draw information
    team_names = list(result.keys())[:-3]  # Exclude 'Drawn' and 'Winning Team'
    team1_name, team2_name = team_names
    draw = result['Drawn']
    winning_team = result['Winning Team']
    losing_team = result['Losing Team']


    new_result = {
        'Team1': f"{team1_name} ({result[team1_name]})",
        'Team2': f"{team2_name} ({result[team2_name]})",
        'Drawn': draw,
        'Winning Team': winning_team,
        "Losing Team": losing_team
    }
    restructured_list.append(new_result)

df = pd.DataFrame(restructured_list)
df.columns = ['Team1', 'Team2', 'Drawn', 'Winning Team', 'Losing Team']
if not os.path.exists('result_list_round_8.xlsx'):
    df.to_excel('result_list_round_8.xlsx', index=False, engine='openpyxl')

dict_list = {"currentWeek": current_matchweek, 
             "matchupData": []}

for obj in clean_list:
    dict_list['matchupData'].append(obj.dic)
    
print(dict_list)

# print(type(dict_list))
# for item in dict_list:
#     print(type(item))

app = Flask(__name__)
CORS(app)
app.secret_key = "AKL95Pegasus"
proper_matchup = []

@app.route("/", methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        proper_matchup.clear()
        session['team1'] = request.form['team1']
        session['team2'] = request.form['team2']
        team1 = next((p for p in clean_list if str(p.name) == str(request.form.get("team1"))), None)
        team2 = next((p for p in clean_list if str(p.name) == str(request.form.get("team2"))), None)
        proper_matchup.append([team1, team2])
        return redirect(url_for("matchup_table"))     
    return render_template('table.html', battles=proper_matchup, list_options=clean_list, week=current_matchweek)

@app.route("/matchup", methods=['GET', 'POST'])
def matchup_table():
    data = request.args.get('hidden_data')
    if data:
        sched_battle = data.split('^')
    else:
        sched_battle = []
    return render_template('table.html', battles=proper_matchup, default=sched_battle, list_options=clean_list, week=current_matchweek)

@app.route("/matchup-api", methods=['GET', 'POST'])
def matchup_api():
    return jsonify(dict_list)

@app.route("/schedule", methods=['GET', 'POST'])
def schedule_page():
    return render_template('schedule.html', matchups=round_1_matchups, letters=paired_letters)

@app.route("/api-schedule", methods=['GET', 'POST'])
def api_schedule():
    matchups_dicts = [{"Team1": matchup[0], "Team2": matchup[1]} for matchup in round_1_matchups]
    return jsonify(matchups_dicts)

@app.route("/refresh", methods=['POST'])
def refresh_page():
    received_key = request.form.get('secret_key', None)
    if received_key == os.environ.get("SECRET_KEY"):
        update(current_matchweek, leagues)
        return jsonify({"message": "Data updated successfully"}), 200
    else:
        return jsonify({"error": "Invalid secret key"}), 403

@app.route("/winners", methods=["GET"])
def winners_page():
    return render_template('winners.html', data=data_list)

@app.route("/winners-api", methods=["GET"])
def winners_api():
    return jsonify(data_list)

@app.route("/rankings", methods=["GET"])
def rankings_page():
    default_week = current_matchweek  
    selected_week = request.args.get('week', default_week)
    try:
        selected_week = int(selected_week)
    except (ValueError, TypeError):
        selected_week = default_week  
    weeks = [str(i) for i in range(1, current_matchweek+1)]
    conn = get_db_connection()
    cursor = conn.cursor()
    # Query the database for rankings for the specified week
    query = """
        SELECT t.team_name, m.score, m.league, m.week
        FROM matchup_rankings.matchups m
        JOIN matchup_rankings.teams t ON m.team_id = t.team_id
        WHERE m.week = %s;
        """
    cursor.execute(query, (selected_week,))
    rankings = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert query results to a list of dictionaries
    rankings_list = [{'team_id': row[0], 'score': row[1], 'league': row[2], 'week': row[3]} for row in rankings]
    
    # rankings_data =  jsonify(rankings_list)
    # rankings_data = rankings_data.json()
    rankings_data = process_rankings(rankings_list)
    # rankings_data = get_rankings(selected_week-1)
    return render_template('new_rankings.html', data=rankings_data, weeks=weeks, matchweek=selected_week)

@app.route('/api_rankings', methods=['GET'])
def api_rankings():
    # week = request.args.get('week')  # Get 'week' from query parameter
    # if not week:
    #     return jsonify({'error': 'Week parameter is required'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    # Query the database for rankings for the specified week
    query = """
        SELECT t.team_name, m.score, m.league, m.week
        FROM matchup_rankings.matchups m
        JOIN matchup_rankings.teams t ON m.team_id = t.team_id
        """
    cursor.execute(query)
    rankings = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert query results to a list of dictionaries
    rankings_list = [{'team_id': row[0], 'score': row[1], 'league': row[2], 'week': row[3]} for row in rankings]
    
    return jsonify(rankings_list)
    
# @scheduler.task('interval', id='do_job_1', seconds=60*30, misfire_grace_time=900)
# def job1():
#     print("Job running")
#     update(current_matchweek, leagues)

if __name__ == '__main__':
    app.run(debug=True, port=3000)