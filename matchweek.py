from dataclasses import dataclass
from depen import *
from datetime import datetime
import pandas as pd

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%a, %b %d, %Y")
    except ValueError:
        return None

def assign_matchweek():
    matchweek_ranges = {
        1: ("2023-10-24", "2023-10-29"),
        2: ("2023-10-30", "2023-11-05"),
        3: ("2023-11-06", "2023-11-12"),
        4: ("2023-11-13", "2023-11-19"),
        5: ("2023-11-20", "2023-11-26"),
        6: ("2023-11-27", "2023-12-03"),
        7: ("2023-12-04", "2023-12-10"),
        8: ("2023-12-11", "2023-12-17"),
        9: ("2023-12-18", "2023-12-24"),
        10: ("2023-12-25", "2023-12-31"),
        11: ("2024-01-01", "2024-01-07"),
        12: ("2024-01-08", "2024-01-14"),
        13: ("2024-01-15", "2024-01-21"),
        14: ("2024-01-22", "2024-01-28"),
        15: ("2024-01-29", "2024-02-04"),
        16: ("2024-02-05", "2024-02-11"),
        17: ("2024-02-12", "2024-02-25"),
        18: ("2024-02-26", "2024-03-03"),
        19: ("2024-03-04", "2024-03-10"),
        20: ("2024-03-11", "2024-03-17"),
    }
    today = datetime.today().date()
    # Iterate over the matchweek_ranges to find the matchweek
    for matchweek, (start_date, end_date) in matchweek_ranges.items():
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        # Check if today's date falls within the range
        if start_date <= today <= end_date:
            return matchweek
    return None

def build_date_table(): 
    date_df = pd.read_csv('Schedule Table.csv')
    date_df['Date_Corrected'] = date_df['Date'].apply(parse_date)
    date_df["matchweek"] = date_df["Date_Corrected"].apply(assign_matchweek)

    return date_df

