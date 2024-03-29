# from flask import Flask, request, jsonify, Blueprint
# import psycopg2
# from depen import get_db_connection

# api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# @api_blueprint.route('/get_rankings', methods=['GET'])
# def get_rankings():
#     print("GOT HERE")
#     week = request.args.get('week')  # Get 'week' from query parameter

#     if not week:
#         return jsonify({'error': 'Week parameter is required'}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Query the database for rankings for the specified week
#     query = """
#         SELECT t.team_name, m.score, m.league, m.week
#         FROM matchup_rankings.matchups m
#         JOIN matchup_rankings.teams t ON m.team_id = t.team_id
#         WHERE m.week = %s;
#         """
#     cursor.execute(query, (week,))
#     rankings = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     # Convert query results to a list of dictionaries
#     rankings_list = [{'team_id': row[0], 'score': row[1], 'league': row[2], 'week': row[3]} for row in rankings]
    
#     return jsonify(rankings_list)