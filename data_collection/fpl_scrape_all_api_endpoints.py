import requests
import pandas as pd

# Base URL for the FPL API
base_url = "https://fantasy.premierleague.com/api/"

# Endpoints as per the provided document
endpoints = {
    "bootstrap_static": "bootstrap-static/",
    "my_team": "my-team/1487607/",  # replace <team_id> with your actual team ID
    "player": "element-summary/<player_id>/",  # replace <player_id> with actual player ID
    "fixtures": "fixtures/",
    "live": "event/<event_id>/live",  # replace <event_id> with actual event ID
    "transfers": "entry/<entry_id>/transfers",  # replace <entry_id> with actual entry ID
    # "leagues_classic_standings": "leagues-classic/<league_id>/standings/",  # replace <league_id> with actual league ID
    # "leagues_h2h_standings": "leagues-h2h/<league_id>/standings/",  # replace <league_id> with actual league ID
    "event_status": "event-status/"
}

# Create a dictionary to store the data from each endpoint
data = {}

# Fetch data from each endpoint
for name, endpoint in endpoints.items():
    response = requests.get(base_url + endpoint)
    data[name] = response.json()

# Convert the data to DataFrames and save to CSV files
for name, content in data.items():
    df = pd.json_normalize(content)  # flatten the JSON into a DataFrame
    df.to_csv(f"{name}.csv", index=False)
