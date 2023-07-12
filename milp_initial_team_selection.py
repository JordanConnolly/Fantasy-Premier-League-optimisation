import pandas as pd
import pulp as p


def pre_process_data(filename="player_data_22-23.csv", opt_target="Total Points"):
    # Read the CSV file into a DataFrame
    player_attributes = pd.read_csv(filename)
    
    # Convert the position numbers to names
    player_attributes["Position"] = player_attributes["Position"].apply(
        lambda x: "Goalkeeper" if x == 1 else "Defender" if x == 2 else "Midfielder" if x == 3 else "Forward"
    )
    
    # Rename the columns for clarity
    player_attributes.rename(columns={"Name": "Player", "Cost": "Price", "Team": "Team", opt_target: "Value"}, inplace=True)

    return player_attributes


def find_optimal_team(players_df, opt_target):
    # Create dictionaries for player values and prices
    values = players_df.set_index('Player')['Value'].to_dict()
    prices = players_df.set_index('Player')['Price'].to_dict()

    # Create lists of players per position
    gks = players_df.loc[players_df['Position'] == 'Goalkeeper', 'Player'].tolist()
    defs = players_df.loc[players_df['Position'] == 'Defender', 'Player'].tolist()
    mfs = players_df.loc[players_df['Position'] == 'Midfielder', 'Player'].tolist()
    fwds = players_df.loc[players_df['Position'] == 'Forward', 'Player'].tolist()

    # Create lists of players per team
    teams_list = players_df['Team'].unique().tolist()
    team_players_dict = players_df.groupby('Team')['Player'].apply(list).to_dict()

    # Create the problem and set it to maximization (we want to maximize value)
    prob = p.LpProblem("The FPL problem", p.LpMaximize)

    # Create the dictionaries to contain the referenced player variables
    gk_vars = p.LpVariable.dicts("gk", gks, cat=p.LpBinary)
    def_vars = p.LpVariable.dicts("df", defs, cat=p.LpBinary)
    mf_vars = p.LpVariable.dicts("mf", mfs, cat=p.LpBinary)
    fwds_vars = p.LpVariable.dicts("fwd", fwds, cat=p.LpBinary)
    all_player_vars = {**gk_vars, **def_vars, **mf_vars, **fwds_vars}

    # Create the objective
    prob += p.lpSum([values[i]*all_player_vars[i] for i in players_df['Player'].tolist()]), "Value objective"

    # Create the constraints
    prob += p.lpSum([gk_vars[i] for i in gks]) == 2, "Number of goalkeepers wanted"
    prob += p.lpSum([def_vars[i] for i in defs]) == 5, "Number of defenders wanted"
    prob += p.lpSum([mf_vars[i] for i in mfs]) == 5, "Number of midfielders wanted"
    prob += p.lpSum([fwds_vars[i] for i in fwds]) == 3, "Number of forwards wanted"
    prob += p.lpSum([prices[i]*all_player_vars[i] for i in players_df['Player'].tolist()]) <= 100, "Price constraint"
    for team in teams_list:
        prob += p.lpSum([all_player_vars[i] for i in team_players_dict[team]]) <= 3, f"Max per {team} constraint"

    # Solve the problem
    prob.solve()

    # Assign the status of the problem
    status = p.LpStatus[prob.status]

    # Put the selected player names to a list
    best_15 = [v.name for v in prob.variables() if v.varValue > 0]

    # Put the correct player names to a list
    inv_player_names = {v.name: k for k, v in all_player_vars.items()}
    best_15_corrected = [inv_player_names[player] for player in best_15]

    # Assign the total price
    total_price = sum(prices[player] for player in best_15_corrected)

    # Assign the player stats
    best_15_positions = players_df.set_index('Player').loc[best_15_corrected, 'Position'].tolist()
    best_15_prices = players_df.set_index('Player').loc[best_15_corrected, 'Price'].tolist()
    best_15_target_values = players_df.set_index('Player').loc[best_15_corrected, 'Value'].tolist()

    # Assign the total value
    total_value = p.value(prob.objective)

    # Create the dataframe to return
    result_df = pd.DataFrame({
        'player': best_15_corrected,
        'position': best_15_positions,
        'price': [round(p, 2) for p in best_15_prices],
        'target_value': best_15_target_values,
        'type': ['Player'] * len(best_15_corrected),  # New 'type' column
    })
    total_stats = pd.DataFrame({
        'player': ['Opt_Status', 'Opt_Target', 'Total_Price', 'Total_Target_Value'],
        'position': [status, opt_target, round(total_price, 2), round(total_value, 2)],
        'type': ['Statistic'] * 4,  # New 'type' column
    })

    # Concatenate the two dataframes
    result_df = pd.concat([result_df, total_stats])

    return result_df


player_attributes = pre_process_data("player_data_22-23.csv", "Total Points")
opt_target = "Total Points"
result_df = find_optimal_team(player_attributes, opt_target)

print(result_df)