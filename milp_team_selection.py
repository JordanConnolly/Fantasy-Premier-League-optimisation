from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value, LpStatus
import pandas as pd

# Read player data from CSV
player_data = pd.read_csv("player_data_22-23.csv")
print(player_data.columns)

# Create a dictionary of player data for each player
player_data_dict = {}
for i in range(len(player_data)):
    player_data_dict[player_data["Player ID"][i]] = {
        "Name": player_data["Name"][i],
        "Team": player_data["Team"][i],
        "Position": player_data["Position"][i],
        "Cost": player_data["Cost"][i],
        "Total Points": player_data["Total Points"][i],
        "Minutes": player_data["Minutes"][i],
        "Goals Scored": player_data["Goals Scored"][i],
        "Assists": player_data["Assists"][i],
        "Clean Sheets": player_data["Clean Sheets"][i],
        "Selected By %": player_data["Selected By %"][i],
        "ROI": player_data["ROI"][i],
        "Points per Minute": player_data["Points per Minute"][i],
        "PpM ROI": player_data["PpM ROI"][i]
    }

budget = 84

# Determine unique teams and set team limits
team_limits = {}
unique_teams = player_data["Team"].unique()
for team in unique_teams:
    team_limits[team] = 3

team_position_limits = {
    "GK": {"min": 1},
    "DEF": {"min": 4},
    "MID": {"min": 4},
    "FWD": {"min": 2}
}

# Create the LP problem
problem = LpProblem("FPL_Team_Selection", LpMaximize)

# Create the decision variables
players = player_data_dict  # Assign the player data dictionary to 'players'
selection = LpVariable.dicts("selection", players, cat='Binary')

# Add the team constraints
for team in unique_teams:
    problem += lpSum([selection[i] for i in players if players[i]["Team"] == team]) <= team_limits[team]

# Add the player constraints
problem += lpSum(selection[i] for i in players) == 11

# Add the position constraints
for position, limit in team_position_limits.items():
    problem += lpSum([selection[i] for i in players if players[i]["Position"] == position]) >= limit["min"]

# Add the objective function to the problem
problem += lpSum([players[i]["PpM ROI"] * selection[i] for i in players])

# Add the total cost constraint
problem += lpSum([players[i]["Cost"] * selection[i] for i in players]) <= budget

# Solve the problem
problem.solve()

# Print the status of the solution
print("Status:", LpStatus[problem.status])

# Print why the solution is infeasible
if LpStatus[problem.status] == "Infeasible":
    print("Infeasible because:")
    for constraint in problem.constraints:
        print(constraint, ":", problem.constraints[constraint].pi)

# Initialise total cost and create lists for each attribute
total_cost = 0
names = []
teams = []
positions = []
costs = []

# Collect the optimal team information
for i in players:
    if selection[i].value() == 1:
        names.append(players[i]["Name"])
        teams.append(players[i]["Team"])
        positions.append(players[i]["Position"])
        costs.append(players[i]["Cost"])
        total_cost += players[i]["Cost"]

# Create a DataFrame for the optimal team
optimal_team_df = pd.DataFrame({
    "Name": names,
    "Team": teams,
    "Position": positions,
    "Cost": costs
})

# Print the optimal team
print("Optimal Team:")
print(optimal_team_df)

# Print the total cost of the optimal team
print("Total Cost: {}M".format(total_cost))
