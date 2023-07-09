import requests
import plotly.express as px
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

    # Iterate over the players
    for player in players:
        player_id = player["id"]
        player_cost = player["now_cost"] / 10  # Divide by 10 to get the actual cost
        player_point = player["total_points"]
        player_name = player["web_name"]
        player_team = data["teams"][player["team"] - 1]["name"]
        player_position = player["element_type"]
        player_minute = player["minutes"]

        # Append player information to the lists
        player_ids.append(player_id)
        player_costs.append(player_cost)
        player_points.append(player_point)
        player_names.append(player_name)
        player_teams.append(player_team)
        player_positions.append(player_position)
        player_minutes.append(player_minute)

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
        }
    )

    # Calculate ROI (Return on Investment)
    player_df["ROI"] = player_df["Total Points"] / player_df["Cost"]

    # Calculate Points per Minute
    player_df["Points per Minute"] = player_df["Total Points"] / player_df["Minutes"]

    # Filter the DataFrame to include only players with more than 50 minutes
    player_df = player_df[player_df["Minutes"] > 500]

    # Create a scatter plot using Plotly for the non-dominated individuals
    fig = px.scatter(
        player_df,
        x="Points per Minute",
        y="Total Points",
        color="Total Points",  # Color markers by points
        symbol="Position",  # Use different marker types for position
        hover_data=[
            "Player ID",
            "Name",
            "Team",
            "Position",
            "ROI",
            "Minutes",
            "Points per Minute"
        ],  # Include ROI and Minutes in hover data
        labels={
            "Cost": "Cost (£ million)",
            "Total Points": "Total Points",
            "ROI": "Return on Investment",
            "Points per Minute": "Points per Minute"
        },
        title="Player Cost vs ROI",
        color_continuous_scale="plasma_r",  # Reversed color scale
    )

    # Set axis labels and title
    fig.update_layout(
        xaxis_title="X",
        yaxis_title="Y",
        legend_title="Legend",
    )

    # Move the legend to the top-right position
    fig.update_layout(
        legend=dict(orientation="h", yanchor="top", y=1.02, xanchor="right", x=1)
    )

    # Add a drop-down box to select and filter by position
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list(
                    [
                        dict(
                            label="All",
                            method="update",
                            args=[
                                {"visible": [True, True, True, True]},
                                {"title": "All Players"},
                            ],
                        ),
                        dict(
                            label="Goalkeepers",
                            method="update",
                            args=[
                                {"visible": [True, False, False, False]},
                                {"title": "Goalkeepers"},
                            ],
                        ),
                        dict(
                            label="Defenders",
                            method="update",
                            args=[
                                {"visible": [False, True, False, False]},
                                {"title": "Defenders"},
                            ],
                        ),
                        dict(
                            label="Midfielders",
                            method="update",
                            args=[
                                {"visible": [False, False, True, False]},
                                {"title": "Midfielders"},
                            ],
                        ),
                        dict(
                            label="Forwards",
                            method="update",
                            args=[
                                {"visible": [False, False, False, True]},
                                {"title": "Forwards"},
                            ],
                        ),
                    ]
                ),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.0,
                xanchor="right",
                y=1.1,
                yanchor="top",
            )
        ]
    )

    # Show the interactive plot
    fig.show()

else:
    # Print an error message if the request was unsuccessful
    print("Failed to retrieve player data from the API.")
