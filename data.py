import psycopg2

def get_team_id(team_name, cursor):
        cursor.execute("SELECT team_id FROM matchup_rankings.teams WHERE team_name = %s;", (team_name,))
        result = cursor.fetchone()
        return result[0] if result else None

def update_db_rankings(df):
    # connect to postgresql
    conn = psycopg2.connect(database="db_191_bball_db",
                        host="dpg-ciue2hdgkuvoig81jpdg-a.singapore-postgres.render.com",
                        user="db_191_bball_db_user",
                        password="quLutlREFgxzM9ngAk6tu8JDcYR3BSOr",
                        port="5432")
    cursor = conn.cursor()

    unique_teams = df['Team'].unique()
    for team in unique_teams:
        cursor.execute("INSERT INTO matchup_rankings.teams (team_name) VALUES (%s) ON CONFLICT (team_name) DO NOTHING;", (team,))

    # Function to get team_id


    # Iterate over DataFrame rows for matchups
    for index, row in df.iterrows():
        team_name = row['Team']
        score = row['Matchups Score']
        league = row['League']
        week = row['Week']

        # Get team_id
        team_id = get_team_id(team_name, cursor)

        # Insert matchup data
        cursor.execute("INSERT INTO matchup_rankings.matchups (team_id, score, league, week) VALUES (%s, %s, %s, %s);", (team_id, score, league, week))

    # Commit transactions and close the connection
    conn.commit()
    cursor.close()
    conn.close()