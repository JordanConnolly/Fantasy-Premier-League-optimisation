import requests
import pandas as pd
from tabulate import tabulate

# Set up the API endpoint URL
url = "https://fantasy.premierleague.com/api/bootstrap-static/"

# Send a GET request to the API endpoint
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the response as JSON
    data = response.json()

    # Extract player data from the response
    players = data["elements"]

    # Create a pandas dataframe
    df = pd.DataFrame(players)
    print(" ")
    print(df.columns)
    print(df.shape)

    # Filter DF to only include players with more than 10 points
    df = df.loc[(df["total_points"] > 10) 
                & (df["minutes"] > 0)]
    print(df.shape)
    
    # Filter DF to only include players selected by more than 10% of players
    df["selected_by_percent"] = df["selected_by_percent"].astype(float)
    df = df.loc[df["selected_by_percent"] > 10]
    print(df.shape)
    
    # Display the full table
    full_table = df[["web_name", "total_points", "minutes", "now_cost", "team", 
                    "chance_of_playing_this_round", "chance_of_playing_next_round"]].sort_values(by="total_points", ascending=False)

    print(tabulate(full_table, headers='keys', tablefmt='fancy_grid'))

    # Display the goalkeepers only
    goalkeepers_table = df.loc[df["element_type"] == 1, ["web_name", "total_points", "minutes", "now_cost", "team", 
                                                        "chance_of_playing_this_round", "chance_of_playing_next_round"]].sort_values(by="total_points", ascending=False)

    print(tabulate(goalkeepers_table, headers='keys', tablefmt='fancy_grid'))

