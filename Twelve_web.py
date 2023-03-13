from flask import Flask, render_template
from espn_api.basketball import League
import pandas as pd
from Twelve_Team_web import Teams

league = League(league_id=359895720, year=2023,
                    espn_s2='AEAPpT2YTAnKfncXZe123FckdpKdvMuwgN8XaFBQNA%2Fx2GuXtzzqjH5luJofsJOjXJdtlbibgvxkGVgI9%2F5KjlbrpyvCOWPUqWyZDGMJXKqDR1yfEHIdCvGpdy3x7lyzjewSeWDCh9%2BEF2UPWJaR2%2Fyj7%2FhEyZ5JNkkngjB8jZOi7ADP410Uq9htyDTm9I%2BNsD3PXjNNyT%2F50j0O7373wXT4TBsNkOFAgG6RtJovex1okSifXZVvG%2FsVzID%2BtFYEamYK7q0mUeQOKiAvjHtOTn3xAeAvcrYmD%2FJrW8pgEk7tY7G6WZJJRKrCOhU6UrDLha6o2BGAtBZS%2B0WIEI%2F%2FI%2Fny',
                    swid='{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}')

score_list = []
team_matchups = []

def pull(matchup_period):
    league = League(league_id=359895720, year=2023,
                    espn_s2='AEAPpT2YTAnKfncXZe123FckdpKdvMuwgN8XaFBQNA%2Fx2GuXtzzqjH5luJofsJOjXJdtlbibgvxkGVgI9%2F5KjlbrpyvCOWPUqWyZDGMJXKqDR1yfEHIdCvGpdy3x7lyzjewSeWDCh9%2BEF2UPWJaR2%2Fyj7%2FhEyZ5JNkkngjB8jZOi7ADP410Uq9htyDTm9I%2BNsD3PXjNNyT%2F50j0O7373wXT4TBsNkOFAgG6RtJovex1okSifXZVvG%2FsVzID%2BtFYEamYK7q0mUeQOKiAvjHtOTn3xAeAvcrYmD%2FJrW8pgEk7tY7G6WZJJRKrCOhU6UrDLha6o2BGAtBZS%2B0WIEI%2F%2FI%2Fny',
                    swid='{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}')
    scoreboard = league.box_scores(matchup_period=matchup_period, scoring_period=1, matchup_total=True)
    score = league.scoreboard(matchupPeriod=matchup_period)

    for items in scoreboard:
        team_matchups.append([items.home_team, {items.away_team}])
    for games in team_matchups:
        games[0] = Teams(mw=matchup_period, player=team_matchups.index(games), place="home", league=league, scoreboard=scoreboard, score=score)
        games[1] = Teams(mw=matchup_period, player=team_matchups.index(games), place="away", league=league, scoreboard=scoreboard, score=score)
        score_list.append(games[0])
        score_list.append(games[1])
pull(15)    

custom_matchups = [["Team(Redfern City Hoopfish)", "Team(Newtown Sugma)"], ["Team(Kobe Wan Ginobi)", "Team(Coomtown  Creambacks )"], ["Team(Orlando Tragic)", "Team(Harden The Fuck Up)"], ["Team(Dallas Luka Deez Nuts)", "Team(New York Dumpsterfires)"]]
new_matchups = []

for teamA in score_list:
    for teamB in score_list:
        for custom in custom_matchups:
            if [str(teamA.name), str(teamB.name)] == custom:
                if [teamA, teamB] not in new_matchups and [teamB, teamA] not in new_matchups:
                    new_matchups.append([teamA, teamB])
            if [str(teamB.name), str(teamA.name)] == custom:
                if [teamA, teamB] not in new_matchups and [teamB, teamA] not in new_matchups:
                    new_matchups.append([teamB, teamA])


app = Flask(__name__)

@app.route("/")
def table():
    return render_template('table.html', battles=new_matchups)

if __name__ == '__main__':
    app.run(debug=True)
