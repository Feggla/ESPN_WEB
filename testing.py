import requests
import pandas as pd
import math

# def fetch_rankings_from_api(week):
#     url = 'https://knockout-comp.onrender.com/api_rankings'  # Replace with your actual API URL
#     params = {'week': int(week)}
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise Exception(f"API request failed with status code {response.status_code}")

def calculate_colors(score, max_score, min_score):
    if math.isnan(score) or math.isnan(max_score) or math.isnan(min_score) or max_score == min_score:
        return 'rgb(255, 255, 255)'
    if max_score == min_score:
        return 'rgb(255, 255, 255)'
    red = 255 - int((score - min_score) / (max_score - min_score) * 255)
    green = int((score - min_score) / (max_score - min_score) * 200)
    return f'rgb({red},{green},0)'

def process_rankings(api_data):
    # Create DataFrame from API data, ensuring column names match the data keys
    print(type(api_data))
    rank_df = pd.DataFrame(api_data)
    rank_df.rename(columns={'team_id': 'Team', 'score': 'Matchups Score', 'league': 'League'}, inplace=True)

    # Clean 'Matchups Score' column, replacing NaN values and converting to float
    rank_df['Matchups Score'] = pd.to_numeric(rank_df['Matchups Score'], errors='coerce')
    rank_df['Matchups Score'].fillna(0, inplace=True)  # Replace NaN with a default score, e.g., 0

    # Calculate min and max scores
    min_score = rank_df['Matchups Score'].min()
    max_score = rank_df['Matchups Score'].max()

    # Apply color calculation
    rank_df['Color'] = rank_df['Matchups Score'].apply(lambda score: calculate_colors(score, max_score, min_score))

    # Sort by 'Matchups Score'
    sorted_rankings = rank_df.sort_values(by='Matchups Score', ascending=False)

    return sorted_rankings.to_dict(orient='records')

# def process_rankings(api_data):
#     print(type(api_data))
#     rank_df = pd.DataFrame(api_data, columns=['Team', 'Matchups Score', 'League', 'Week'])
#     min_score = float(rank_df['Matchups Score'].min())
#     max_score = float(rank_df['Matchups Score'].max())
#     print(type(min_score))
#     rank_df['Color'] = rank_df['Matchups Score'].apply(lambda score: calculate_colors(score, max_score, min_score))
#     sorted_rankings = rank_df.sort_values(by='Matchups Score', ascending=False)
#     return sorted_rankings

def get_rankings(data):
    # data = fetch_rankings_from_api(week)
    sorted_rankings_df = process_rankings(data)
    return sorted_rankings_df