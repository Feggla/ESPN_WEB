from espn_api.basketball import League
from Team_web import Teams
from espn_api.requests.espn_requests import ESPNInvalidLeague
import pandas as pd
from depen import get_db_connection



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

def pull(matchup_period, leagues, year):
    overall_list.clear()
    scoreboards_dic = {}
    for association in leagues:
        team_matchups = []
        score_list = []
        try:
            league = League(league_id=leagues[association]['id'], year=year, espn_s2=leagues[association]['s2'], swid=leagues[association]['swid'])
        except ESPNInvalidLeague:
            print(association, year)
        try:
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
        except (AttributeError, TypeError):
            print(year, week)
        

years = [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008]

records = {
    'points': {'team': '', 'year': 0, 'week': 0, 'league': '', 'score': 0},
    'blocks': {'team': '', 'year': 0, 'week': 0, 'league': '', 'score': 0},
    'steals': {'team': '', 'year': 0, 'week': 0, 'league': '', 'score': 0},
    'assists': {'team': '', 'year': 0, 'week': 0, 'league': '', 'score': 0},
    'rebounds': {'team': '', 'year': 0, 'week': 0, 'league': '', 'score': 0},
    'turnovers': {'team': '', 'year': 0, 'week': 0, 'league': '', 'score': 100},
    'fg': {'team': '', 'year': 0, 'week': 0, 'league': '', 'score': 0},
    'ft': {'team': '', 'year': 0, 'week': 0, 'league': '', 'score': 0},
    'threes': {'team': '', 'year': 0, 'week': 0, 'league': '', 'score': 0},
    'three_percent': {'team': '', 'year': 0, 'week': 0, 'league': '', 'score': 0},
    'td': {'team': '', 'year': 0, 'week': 0, 'league': '', 'score': 0}
}

for year in years:
    for week in range(1,20):
        if year == 2024 and week == 12:
            continue
        pull(week, leagues, year)
        for team in overall_list:
            if team.points > records['points']['score']:
                records['points']['score'] = team.points
                records['points']['team'] = str(team.name)
                records['points']['year'] = year
                records['points']['week'] = week
                records['points']['league'] = team.league

            if team.blocks > records['blocks']['score']:
                records['blocks']['score'] = team.blocks
                records['blocks']['team'] = str(team.name)
                records['blocks']['year'] = year
                records['blocks']['week'] = week
                records['blocks']['league'] = team.league

            if team.steals > records['steals']['score']:
                records['steals']['score'] = team.steals
                records['steals']['team'] = str(team.name)
                records['steals']['year'] = year
                records['steals']['week'] = week
                records['steals']['league'] = team.league

            if team.assists > records['assists']['score']:
                records['assists']['score'] = team.assists
                records['assists']['team'] = str(team.name)
                records['assists']['year'] = year
                records['assists']['week'] = week
                records['assists']['league'] = team.league

            if team.rebounds > records['rebounds']['score']:
                records['rebounds']['score'] = team.rebounds
                records['rebounds']['team'] = str(team.name)
                records['rebounds']['year'] = year
                records['rebounds']['week'] = week
                records['rebounds']['league'] = team.league

            if team.turnovers < records['turnovers']['score']:
                records['turnovers']['score'] = team.turnovers
                records['turnovers']['team'] = str(team.name)
                records['turnovers']['year'] = year
                records['turnovers']['week'] = week
                records['turnovers']['league'] = team.league

            if team.fg > records['fg']['score']:
                records['fg']['score'] = team.fg
                records['fg']['team'] = str(team.name)
                records['fg']['year'] = year
                records['fg']['week'] = week
                records['fg']['league'] = team.league

            if team.ft > records['ft']['score']:
                records['ft']['score'] = team.ft
                records['ft']['team'] = str(team.name)
                records['ft']['year'] = year
                records['ft']['week'] = week
                records['ft']['league'] = team.league

            if team.threes > records['threes']['score']:
                records['threes']['score'] = team.threes
                records['threes']['team'] = str(team.name)
                records['threes']['year'] = year
                records['threes']['week'] = week
                records['threes']['league'] = team.league

            if team.three_percent > records['three_percent']['score']:
                records['three_percent']['score'] = team.three_percent
                records['three_percent']['team'] = str(team.name)
                records['three_percent']['year'] = year
                records['three_percent']['week'] = week
                records['three_percent']['league'] = team.league

            if team.td > records['td']['score']:
                records['td']['score'] = team.td
                records['td']['team'] = str(team.name)
                records['td']['year'] = year
                records['td']['week'] = week
                records['td']['league'] = team.league
        conn = get_db_connection()
        cursor = conn.cursor()
        for category in records:
            existing_score = records[category]['score']
            cursor.execute("""
            UPDATE records.team_scores 
            SET team = %s, year = %s, week = %s, league = %s, score = %s 
            WHERE category = %s AND score != %s;
            """, (records[category]['team'], records[category]['year'], records[category]['week'], records[category]['league'], records[category]['score'], category, existing_score))
            conn.commit()
        cursor.close()
        conn.close()
    print(f"completed year {year}")
    print(records)

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
# df = pd.DataFrame.from_dict(records, orient='index')
# df.reset_index(inplace=True)
# df.rename(columns={'index': 'category'}, inplace=True)
# conn = get_db_connection()
# cursor = conn.cursor()
# for category in records:
#     existing_score = records[category]['score']
#     cursor.execute("""
#                 UPDATE records.team_scores 
#                 SET category = %s, team = %s, year = %s, week = %s, league = %s, score = %s 
#                 WHERE category = %s AND score != %s
#             """, (category, records[category]['team'], records[category]['year'], records[category]['week'], records[category]['league'], records[category]['score'], category, existing_score))
    
# print("COMPLETED RECORDS")
# print(df)
# conn.commit()
# cursor.close()
# conn.close()
