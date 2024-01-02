from espn_api.basketball import League
from espn_api.basketball import Team
from espn_api.basketball import Player
import pandas as pd
import numpy as np
import datetime
import psycopg2
# import pyodbc
import os

league = League(league_id=359895720, year=2024, espn_s2='AEAPpT2YTAnKfncXZe123FckdpKdvMuwgN8XaFBQNA%2Fx2GuXtzzqjH5luJofsJOjXJdtlbibgvxkGVgI9%2F5KjlbrpyvCOWPUqWyZDGMJXKqDR1yfEHIdCvGpdy3x7lyzjewSeWDCh9%2BEF2UPWJaR2%2Fyj7%2FhEyZ5JNkkngjB8jZOi7ADP410Uq9htyDTm9I%2BNsD3PXjNNyT%2F50j0O7373wXT4TBsNkOFAgG6RtJovex1okSifXZVvG%2FsVzID%2BtFYEamYK7q0mUeQOKiAvjHtOTn3xAeAvcrYmD%2FJrW8pgEk7tY7G6WZJJRKrCOhU6UrDLha6o2BGAtBZS%2B0WIEI%2F%2FI%2Fny', swid='{0AF1C993-43AE-4A5A-A6AB-0E7D125A2C96}')

os.environ.get

def get_db_connection():
    conn = psycopg2.connect(database=os.environ.get("database"),
                        host=os.environ.get("host"),
                        user=os.environ.get("user"),
                        password=os.environ.get("password"),
                        port=os.environ.get("port"),
    )
    return conn