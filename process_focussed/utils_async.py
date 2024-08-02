import asyncio
import aiohttp
import pandas as pd
import os
import feedparser
import logging
from argparse import ArgumentParser
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Asynchronous helper function
async def fetch(session, url, params=None):
    async with session.get(url, params=params) as response:
        if response.status != 200:
            logging.error(f"Error fetching {url}: {response.status}")
            return None
        return await response.json()

# FPL data fetching
async def get_fpl_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    async with aiohttp.ClientSession() as session:
        data = await fetch(session, url)
        if not data:
            raise Exception("Failed to retrieve player data from the API.")
        
        players = data["elements"]
        teams = {team['id']: team['name'] for team in data['teams']}
        
        player_data = [{
            "Player ID": player["id"],
            "Name": player["web_name"],
            "Team": teams[player["team"]],
            "Position": player["element_type"],
            "Cost": player["now_cost"] / 10,
            "Total Points": player["total_points"],
            "Minutes": player["minutes"],
            "Goals Scored": player["goals_scored"],
            "Assists": player["assists"],
            "Clean Sheets": player["clean_sheets"],
            "Selected By %": player["selected_by_percent"],
            "Status": player["status"],
        } for player in players]

        player_df = pd.DataFrame(player_data)
        player_df["ROI"] = player_df["Total Points"] / player_df["Cost"]
        player_df["Points per Minute"] = player_df["Total Points"] / player_df["Minutes"].replace(0, 1)
        player_df["PpM ROI"] = player_df["Points per Minute"] * player_df["ROI"]
        player_df = player_df[player_df["Status"] == "a"]

        return player_df

# News data fetching
async def get_news_data():
    news_api_key = os.getenv('NEWS_API_KEY')
    if not news_api_key:
        raise Exception("NewsAPI key not found. Please set the NEWS_API_KEY environment variable.")

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "Premier League OR Fantasy Football",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": news_api_key,
    }
    async with aiohttp.ClientSession() as session:
        data = await fetch(session, url, params)
        if not data:
            raise Exception("Failed to retrieve news data from the API.")
        
        articles = data["articles"]
        for article in articles:
            article['source_name'] = article['source']['name']
        
        return pd.DataFrame(articles)

# RSS feed fetching
def fetch_rss_news(rss_url):
    feed = feedparser.parse(rss_url)
    return pd.DataFrame(feed.entries)

# Main function
async def main(args):
    try:
        player_df = await get_fpl_data()
        logging.info("Successfully retrieved player data from the API.")

        news_df = await get_news_data()
        logging.info("Successfully retrieved news data from the API.")

        rss_df = fetch_rss_news(args.rss_url)
        logging.info("Successfully retrieved RSS news data.")

        # Save the DataFrames
        player_df.to_csv(args.player_output, index=False)
        news_df.to_csv(args.news_output, index=False)
        rss_df.to_csv(args.rss_output, index=False)

        # Filter relevant news
        players_and_teams = set(player_df["Name"]).union(set(player_df["Team"]))
        
        def check_content(content, names):
            if isinstance(content, str):
                return any(name.lower() in content.lower() for name in names)
            return False

        relevant_news_df = news_df[
            news_df["description"].apply(lambda desc: check_content(desc, players_and_teams)) |
            news_df["content"].apply(lambda content: check_content(content, players_and_teams))
        ]
        relevant_news_df = relevant_news_df.drop_duplicates(subset="description")
        relevant_news_df.to_csv(args.filtered_news_output, index=False)

        logging.info("Data processing completed successfully.")

        # Basic data analysis
        print("\nTop 20 players by ROI:")
        print(player_df.sort_values("ROI", ascending=False).head(20)[["Name", "Team", "Cost", "Total Points", "ROI"]])

        print("\nMost mentioned players/teams in news:")
        mentions = relevant_news_df["description"].apply(lambda desc: [name for name in players_and_teams if isinstance(desc, str) and name.lower() in desc.lower()])
        mentions = [item for sublist in mentions for item in sublist]
        print(pd.Series(mentions).value_counts().head(20))

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    parser = ArgumentParser(description="Fetch and process FPL and news data")
    parser.add_argument("--rss_url", default="http://feeds.bbci.co.uk/sport/football/rss.xml", help="RSS feed URL")
    parser.add_argument("--player_output", default="player_data.csv", help="Output file for player data")
    parser.add_argument("--news_output", default="raw_news_data.csv", help="Output file for raw news data")
    parser.add_argument("--rss_output", default="rss_news_data.csv", help="Output file for RSS news data")
    parser.add_argument("--filtered_news_output", default="filtered_news_data.csv", help="Output file for filtered news data")
    args = parser.parse_args()

    asyncio.run(main(args))