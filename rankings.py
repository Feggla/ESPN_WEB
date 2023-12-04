
def check_scores(cat, teamA, teamB, matchup):
    if cat == "turnovers":
        if getattr(teamA, cat) > getattr(teamB, cat):
            matchup[teamB.name] += 1
        if getattr(teamB, cat) > getattr(teamA, cat):
            matchup[teamA.name] += 1
        if getattr(teamA, cat) == getattr(teamB, cat):
            pass
    if cat != "turnovers":
        if getattr(teamA, cat) > getattr(teamB, cat):
            matchup[teamA.name] += 1
        if getattr(teamB, cat) > getattr(teamA, cat):
            matchup[teamB.name] += 1
        if getattr(teamA, cat) == getattr(teamB, cat):
            pass

df_dic = {}

def check_rankings(score_list):
    for teamA in score_list:
        score = 0
        draw = 0
        for teamB in score_list:
            matchup = {teamA.name: 0,
                    teamB.name: 0
                    }
            if teamA != teamB:
                check_scores('points', teamA, teamB, matchup)
                check_scores('blocks', teamA, teamB, matchup)
                check_scores('steals', teamA, teamB, matchup)
                check_scores('assists', teamA, teamB, matchup)
                check_scores('rebounds', teamA, teamB, matchup)
                check_scores('turnovers', teamA, teamB, matchup)
                check_scores('fg', teamA, teamB, matchup)
                check_scores('ft', teamA, teamB, matchup)
                check_scores('threes', teamA, teamB, matchup)
                check_scores('three_percent', teamA, teamB, matchup)
                check_scores('td', teamA, teamB, matchup)
                if matchup[teamA.name] > matchup[teamB.name]:
                    score += 1
                if matchup[teamA.name] == matchup[teamB.name]:
                    draw += 1
        df_dic[teamA.name] = [score, draw, teamA.league]
        # print(f"{teamA.name} would have won {score} and drawn {draw} matchups this week")
    return df_dic

