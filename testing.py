import requests
import pandas as pd

# def fetch_rankings_from_api(week):
#     url = 'http://localhost:5000/rankings'  # Replace with your actual API URL
#     params = {'week': int(week)}
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise Exception(f"API request failed with status code {response.status_code}")

def calculate_colors(score, max_score, min_score):
    if max_score == min_score:
        return 'rgb(255, 255, 255)'
    red = 255 - int((score - min_score) / (max_score - min_score) * 255)
    green = int((score - min_score) / (max_score - min_score) * 200)
    return f'rgb({red},{green},0)'

def process_rankings(api_data):
    rank_df = pd.DataFrame(api_data, columns=['Team', 'Matchups Score', 'League', 'Week'])
    min_score = float(rank_df['Matchups Score'].min())
    max_score = float(rank_df['Matchups Score'].max())
    rank_df['Color'] = rank_df['Matchups Score'].apply(lambda score: calculate_colors(score, max_score, min_score))
    sorted_rankings = rank_df.sort_values(by='Matchups Score', ascending=False)
    return sorted_rankings

def get_rankings(week, data):
    # api_data = fetch_rankings_from_api(week)
    sorted_rankings_df = process_rankings(data)
    return sorted_rankings_df