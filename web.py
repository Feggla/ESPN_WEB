from flask import Flask, render_template, url_for, redirect, request
from espn_api.basketball import League
import pandas as pd
from Team_web import Teams


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
    }
}

scoreboards_dic = {}
overall_list = []

def pull(matchup_period, leagues):
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
            overall_list.append(games[0])
            overall_list.append(games[1])
            score_list.append(games[0])
            score_list.append(games[1])

pull(1, leagues)    

custom_matchups = [["Scottie Pippings", "Dort  Stop Believin"], ["New Orleans Zionlyfans", "Mos Eisley Banthas"], ["Team(Mos Eisley Banthas)", "Team(Dort  Stop Believin)"], ["Team(Dort  Stop Believin)", "Team(New Orleans Zionlyfans)"]]
new_matchups = []
clean_list = []

for team in overall_list:
    team.name = str(team.name).replace("Team(", "").replace(")", "")
    clean_list.append(team)

clean_list = sorted(clean_list, key=lambda team: team.name)

for teamA in overall_list:
    for teamB in overall_list:
        for custom in custom_matchups:
            if [str(teamA.name), str(teamB.name)] == custom:
                if [teamA, teamB] not in new_matchups and [teamB, teamA] not in new_matchups:
                    new_matchups.append([teamA, teamB])
            if [str(teamB.name), str(teamA.name)] == custom:
                if [teamA, teamB] not in new_matchups and [teamB, teamA] not in new_matchups:
                    new_matchups.append([teamB, teamA])



app = Flask(__name__)

proper_matchup = []

@app.route("/", methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        proper_matchup.clear()
        team1 = next((p for p in overall_list if str(p.name) == str(request.form.get("team1"))), None)
        team2 = next((p for p in overall_list if str(p.name) == str(request.form.get("team2"))), None)
        proper_matchup.append([team1, team2])
        return redirect(url_for("matchup_table"))     
    return render_template('table.html', battles=proper_matchup, list_options=clean_list)

@app.route("/matchup", methods=['GET', 'POST'])
def matchup_table():
    return render_template('table.html', battles=proper_matchup, list_options=clean_list)

if __name__ == '__main__':
    app.run(debug=True)
