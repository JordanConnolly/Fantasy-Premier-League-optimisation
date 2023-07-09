import requests
import pandas as pd

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

    # Lists to store player information
    player_ids = []
    player_costs = []
    player_points = []
    player_names = []
    player_teams = []
    player_positions = []
    player_minutes = []
    player_goals_scored = []
    player_assists = []
    player_clean_sheets = []
    player_selected_by_percent = []

    # Iterate over the players
    for player in players:
        player_id = player["id"]
        player_cost = player["now_cost"] / 10  # Divide by 10 to get the actual cost
        player_point = player["total_points"]
        player_name = player["web_name"]
        player_team = data["teams"][player["team"] - 1]["name"]
        player_position = player["element_type"]
        player_minute = player["minutes"]
        player_goals = player["goals_scored"]
        player_assist = player["assists"]
        player_clean_sheet = player["clean_sheets"]
        player_selected_by = player["selected_by_percent"]

        # Append player information to the lists
        player_ids.append(player_id)
        player_costs.append(player_cost)
        player_points.append(player_point)
        player_names.append(player_name)
        player_teams.append(player_team)
        player_positions.append(player_position)
        player_minutes.append(player_minute)
        player_goals_scored.append(player_goals)
        player_assists.append(player_assist)
        player_clean_sheets.append(player_clean_sheet)
        player_selected_by_percent.append(player_selected_by)

    # Create a DataFrame to store player information
    player_df = pd.DataFrame(
        {
            "Player ID": player_ids,
            "Name": player_names,
            "Team": player_teams,
            "Position": player_positions,
            "Cost": player_costs,
            "Total Points": player_points,
            "Minutes": player_minutes,
            "Goals Scored": player_goals_scored,
            "Assists": player_assists,
            "Clean Sheets": player_clean_sheets,
            "Selected By %": player_selected_by_percent,
        }
    )

    # Calculate ROI (Return on Investment)
    player_df["ROI"] = player_df["Total Points"] / player_df["Cost"]

    # Calculate Points per Minute
    player_df["Points per Minute"] = player_df["Total Points"] / player_df["Minutes"]

    # Calculate Points per Minute * ROI
    player_df["PpM ROI"] = (
        player_df["Total Points"] / player_df["Minutes"]
    ) * player_df["ROI"]

    # Filter the DataFrame to include only players with more than 50 minutes
    player_df = player_df[player_df["Minutes"] > 500]

    # Save the DataFrame as a CSV file
    player_df.to_csv("player_data_22-23.csv", index=False)

    # print player_df looping over position; sorted by Points per Minute ROI
    for position in player_df["Position"].unique():
        print(f"\nPosition: {position}")
        print(
            player_df[player_df["Position"] == position].sort_values(
                "PpM ROI", ascending=False
            )
        )

    # Print a success message if the request was successful
    print()
    print("Successfully retrieved player data from the API.")

else:
    # Print an error message if the request was unsuccessful
    print("Failed to retrieve player data from the API.")
