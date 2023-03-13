import pytz
from espn_api.basketball import League
import datetime
import smtplib
from pytz import timezone
import pandas as pd

class Leagues:
    def __init__(self, id, s2, swid):
        self.league = League(league_id=id, year=2023, espn_s2=s2, swid=swid)


class Teams:
    def __init__(self, mw, player, place, league, scoreboard, score):
        self.mw = mw
        self.league = league
        self.scoreboard = scoreboard
        self.score = score
        self.dic = {}
        self.player = player
        self.name = ""
        self.points = 0
        self.blocks = 0
        self.steals = 0
        self.assists = 0
        self.rebounds = 0
        self.turnovers = 0
        self.fg = 0.0
        self.ft = 0.0
        self.threes = 0
        self.three_percent = 0
        self.td = 0
        if place == "home":
            self.stats_home()
        if place == "away":
            self.stats_away()
        self.stat_list = [self.name, self.points, self.blocks, self.steals, self.assists, self.rebounds, self.turnovers, self.fg, self.ft, self.threes]


    def stats_home(self):
        self.name = self.score[self.player].home_team
        self.points = int(self.score[self.player].home_team_cats["PTS"]['score'])
        self.blocks = int(self.score[self.player].home_team_cats["BLK"]['score'])
        self.steals = int(self.score[self.player].home_team_cats["STL"]['score'])
        self.assists = int(self.score[self.player].home_team_cats["AST"]['score'])
        self.rebounds = int(self.score[self.player].home_team_cats["REB"]['score'])
        self.turnovers = int(self.score[self.player].home_team_cats["TO"]['score'])
        self.fg = self.score[self.player].home_team_cats["FG%"]['score']
        self.ft = self.score[self.player].home_team_cats["FT%"]['score']
        self.threes = int(self.score[self.player].home_team_cats["3PTM"]['score'])
        self.dic[self.scoreboard[self.player].home_team] = {
            "PTS": self.score[self.player].home_team_cats["PTS"],
            "BLK": self.score[self.player].home_team_cats["BLK"],
            "STL": self.score[self.player].home_team_cats["STL"],
            "AST": self.score[self.player].home_team_cats["AST"],
            "REB": self.score[self.player].home_team_cats["REB"],
            "TO": self.score[self.player].home_team_cats["TO"],
            "FG%": self.score[self.player].home_team_cats["FG%"],
            "FT%": self.score[self.player].home_team_cats["FT%"],
            "3PTM": self.score[self.player].home_team_cats["3PTM"]
        }

    def stats_away(self):
        self.name = self.score[self.player].away_team
        self.points = int(self.score[self.player].away_team_cats["PTS"]['score'])
        self.blocks = int(self.score[self.player].away_team_cats["BLK"]['score'])
        self.steals = int(self.score[self.player].away_team_cats["STL"]['score'])
        self.assists = int(self.score[self.player].away_team_cats["AST"]['score'])
        self.rebounds = int(self.score[self.player].away_team_cats["REB"]['score'])
        self.turnovers = int(self.score[self.player].away_team_cats["TO"]['score'])
        self.fg = self.score[self.player].away_team_cats["FG%"]['score']
        self.ft = self.score[self.player].away_team_cats["FT%"]['score']
        self.threes = int(self.score[self.player].away_team_cats["3PTM"]['score'])
        self.dic[self.scoreboard[self.player].away_team] = {
            "PTS": self.score[self.player].away_team_cats["PTS"],
            "BLK": self.score[self.player].away_team_cats["BLK"],
            "STL": self.score[self.player].away_team_cats["STL"],
            "AST": self.score[self.player].away_team_cats["AST"],
            "REB": self.score[self.player].away_team_cats["REB"],
            "TO": self.score[self.player].away_team_cats["TO"],
            "FG%": self.score[self.player].away_team_cats["FG%"],
            "FT%": self.score[self.player].away_team_cats["FT%"],
            "3PTM": self.score[self.player].away_team_cats["3PTM"]
        }
