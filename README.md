# Fantasy-Premier-League-optimisation
</br>

## What is it about
Scripts to optimise my premier league fantasy football team so I don't need to do anything.

## Table of Contents
TBC

## Structure

No current structure. Planned structure is as follows:
1) To gather relevant data sources, such as the FPL API, historical data and potentially news. 
2) Apply mixed-integer linear programming (MILP) approach for initial team selection.
3) Create rolling gameweek on gameweek update scripts.
4) Automate the entire process as much as possible so I don't need to do anything.

## MILP Plan

- Decision Variables: Define binary decision variables for each player, indicating whether they are selected in the team or not.
- Objective Function: Define an objective function that represents the performance you want to maximise.
- Budget Constraint: Ensure that the total cost of selected players does not exceed the budget constraint (100M). This can be formulated as a linear constraint.
- Team Limit Constraint: Incorporate the constraint that the selected team should not exceed the limit of players from a single team.
- Position Constraints: Define constraints to ensure that the number of players selected for each position (e.g., goalkeepers, defenders, midfielders, forwards) matches the required number of players in each position.
- Total Player Constraint: Ensure that the total number of selected players is equal to 15.

Generally speaking: In our problem, we have last seasons data on the players in Fantasy Football. We have from the API, curated a dataset, which is a csv file (player_data_22-23.csv). Within this, we have the following columns: Player ID,Name,Team,Position,Cost,Total Points,Minutes,Goals Scored,Assists,Clean Sheets,Selected By %,ROI,Points per Minute,PpM ROI. We cannot have more than 3 players from a single team. We cannot spend over 100M. We can have a max of 15 Players. We can have a specific formation of players, such as 15 players spread across 2 goalies, 2-5 defenders, 2-5 midfielders, 2-3 forwards. We want to maximise the ROI and make sure we spend as little as possible on the best possible bench to maximise money available for the remaining 11 players on field.

## Usage

To run the code use Python and the dependencies in the `requirements.txt` file.

## Dependencies

The code in this repository may have specific dependencies depending on the script. These dependencies are listed in the `requirements.txt` file. Please ensure you have installed the correct dependencies prior to running the code.
