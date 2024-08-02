import requests
import pandas as pd
import os
import feedparser

def get_fpl_data():
    # Set up the Fantasy Premier League API endpoint URL
    fpl_url = "https://fantasy.premierleague.com/api/bootstrap-static/"

    # Send a GET request to the Fantasy Premier League API endpoint
    response = requests.get(fpl_url)

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
        player_statuses = []

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
            player_status = player["status"]

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
            player_statuses.append(player_status)

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
                "Status": player_statuses,
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

        # Filter out players who are unavailable, injured, or suspended
        player_df = player_df[player_df["Status"] == "a"]

        return player_df

    else:
        raise Exception("Failed to retrieve player data from the API.")

def get_news_data():
    # Retrieve the NewsAPI key from the environment variable
    news_api_key = os.getenv('NEWS_API_KEY')

    if not news_api_key:
        raise Exception("NewsAPI key not found. Please set the NEWS_API_KEY environment variable.")

    # Set up the NewsAPI endpoint URL and parameters
    news_api_url = "https://newsapi.org/v2/everything"
    news_params = {
        "q": "Premier League OR Fantasy Football",  # Keywords to search for
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": news_api_key,
    }

    # Send a GET request to the NewsAPI endpoint
    news_response = requests.get(news_api_url, params=news_params)

    # Check if the request was successful (status code 200)
    if news_response.status_code == 200:
        # Parse the response as JSON
        news_data = news_response.json()

        # Extract relevant news articles
        articles = news_data["articles"]

        # Flatten the nested 'source' field
        for article in articles:
            article['source_name'] = article['source']['name']

        # Create a DataFrame for news articles
        news_df = pd.DataFrame(articles)

        return news_df

    else:
        raise Exception("Failed to retrieve news data from the API.")

def fetch_rss_news(rss_url):
    feed = feedparser.parse(rss_url)
    return feed.entries

def fetch_premier_league_news():
    rss_url = 'https://www.premierleague.com/rss'
    feed = feedparser.parse(rss_url)
    
    for entry in feed.entries[:5]:  # Print the first 5 news items
        print(f"Title: {entry.title}")
        print(f"Link: {entry.link}")
        print(f"Published: {entry.published}")
        print(f"Summary: {entry.summary}")
        print("---")

if __name__ == "__main__":
    try:
        # # Get FPL data
        # player_df = get_fpl_data()
        # print("Successfully retrieved player data from the API.")

        # # Get news data
        # news_df = get_news_data()
        # print("Successfully retrieved news data from the API.")

        # Fetch news from RSS feed
        rss_url = 'http://feeds.bbci.co.uk/sport/football/rss.xml'
        rss_news = fetch_rss_news(rss_url)
        print("RSS News:", rss_news)
        
        # # Save the DataFrames as CSV files
        # player_df.to_csv("player_data_23-24.csv", index=False)
        # news_df.to_csv("raw_team_news_23-24.csv", index=False)

        # # Create a list of all player names and team names
        # players_and_teams = set(player_df["Name"]).union(set(player_df["Team"]))

        # # Filter news articles to include only those mentioning players or teams
        # relevant_news_df = news_df[
        #     news_df["description"].apply(lambda desc: any(name in desc for name in players_and_teams)) |
        #     news_df["content"].apply(lambda content: any(name in content for name in players_and_teams))
        # ]

        # # Remove duplicate news entries based on the description
        # relevant_news_df = relevant_news_df.drop_duplicates(subset="description")

        # # Save the filtered news DataFrame
        # relevant_news_df.to_csv("filtered_team_news_23-24.csv", index=False)

        # # Print the filtered news DataFrame
        # print("\nFiltered News Data:")
        # print(relevant_news_df)

    except Exception as e:
        print(str(e))
