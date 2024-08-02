import requests
import pandas as pd
from flask import Flask, render_template, request
from tabulate import tabulate

app = Flask(__name__)

def fetch_data():
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

        return df

@app.route('/')
def index():
    # Fetch data
    df = fetch_data()

    # Apply filters based on user input
    min_points = request.args.get('min_points', type=int) or 10
    min_minutes = request.args.get('min_minutes', type=int) or 0
    min_selection_percent = request.args.get('min_selection_percent', type=float) or 10.0

    filtered_df = df.loc[(df["total_points"] > min_points)
                         & (df["minutes"] > min_minutes)
                         & (df["selected_by_percent"] > min_selection_percent)]

    # Display the filtered table
    table = filtered_df[["web_name", "total_points", "minutes", "now_cost", "team",
                        "chance_of_playing_this_round", "chance_of_playing_next_round"]].sort_values(by="total_points", ascending=False)

    return render_template('index.html', table=table)

if __name__ == '__main__':
    app.run(debug=True)
