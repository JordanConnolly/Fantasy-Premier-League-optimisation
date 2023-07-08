# Fantasy-Premier-League-optimisation
</br>

## What is it about
Scripts to optimise my premier league fantasy football team so I don't need to do anything.

## Table of Contents
TBC

## Structure

No current structure. Planned structure is as follows:
- 1) To gather relevant data sources, such as the FPL API, historical data and potentially news. 
- 2) Apply mixed-integer linear programming (MILP) approach for initial team selection.
- 3) Create rolling gameweek on gameweek update scripts.
- 4) Automate the entire process as much as possible so I don't need to do anything.

## MILP Plan

- Decision Variables: Define binary decision variables for each player, indicating whether they are selected in the team or not.
- Objective Function: Define an objective function that represents the performance you want to maximise.
- Budget Constraint: Ensure that the total cost of selected players does not exceed the budget constraint (100M). This can be formulated as a linear constraint.
- Team Limit Constraint: Incorporate the constraint that the selected team should not exceed the limit of players from a single team.
- Position Constraints: Define constraints to ensure that the number of players selected for each position (e.g., goalkeepers, defenders, midfielders, forwards) matches the required number of players in each position.
- Total Player Constraint: Ensure that the total number of selected players is equal to 15.

## Usage

To run the code use Python and the dependencies in the `requirements.txt` file.

## Dependencies

The code in this repository may have specific dependencies depending on the script. These dependencies are listed in the `requirements.txt` file. Please ensure you have installed the correct dependencies prior to running the code.
