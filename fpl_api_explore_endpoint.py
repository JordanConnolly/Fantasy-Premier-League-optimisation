import requests

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

    # Print all player related data, column by column on each printed row, 
    # for a single player_ID
    for player in players:
        if player["id"] == 1:
            for key, value in player.items():
                print(key, ":", value)
