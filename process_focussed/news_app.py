import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
news_df = pd.read_csv("filtered_team_news_23-24.csv")
player_df = pd.read_csv("player_data_23-24.csv")
raw_news_df = pd.read_csv("raw_team_news_23-24.csv")
rss_df = pd.read_csv("rss_news_data.csv")  # Make sure this file exists

# Function to display news article details
def display_article(df, index):
    st.write(f"### {df.iloc[index]['title']}")
    st.write(f"**Source:** {df.iloc[index].get('source_name', 'N/A')}")
    st.write(f"**Description:** {df.iloc[index].get('description', 'N/A')}")
    st.write(f"**Content:** {df.iloc[index].get('content', df.iloc[index].get('summary', 'N/A'))}")
    url = df.iloc[index].get('url', df.iloc[index].get('link', '#'))
    st.write(f"[Read more]({url})")

# Streamlit app
st.title("Premier League Data Viewer")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["News Viewer", "Player Data", "Data Analysis", "Player Scatterplots", "Player 3D Plots", "RSS Feeds"])

if page == "News Viewer":
    st.header("Premier League News Viewer")
    
    # Choose between filtered and raw news
    news_type = st.radio("Select news type:", ["Filtered News", "Raw News"])
    current_df = news_df if news_type == "Filtered News" else raw_news_df

    # Initialize session state
    if 'index' not in st.session_state:
        st.session_state.index = 0

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Previous"):
            if st.session_state.index > 0:
                st.session_state.index -= 1
    with col3:
        if st.button("Next"):
            if st.session_state.index < len(current_df) - 1:
                st.session_state.index += 1

    # Display the current article
    display_article(current_df, st.session_state.index)

elif page == "Player Data":
    st.header("Player Data")
    
    # Display player data table with sorting and filtering
    st.write("Use the column headers to sort the data. You can also use the search box to filter the data.")
    search = st.text_input("Search players:")
    filtered_df = player_df[player_df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    st.dataframe(filtered_df)

elif page == "Data Analysis":
    st.header("Data Analysis")

    # Player analysis
    st.subheader("Player Analysis")
    metric = st.selectbox("Select metric for top players:", ["Total Points", "ROI", "Goals Scored", "Assists"])
    top_players = player_df.nlargest(10, metric)
    fig = px.bar(top_players, x='Name', y=metric, title=f"Top 10 Players by {metric}")
    st.plotly_chart(fig)

    # Team analysis
    st.subheader("Team Analysis")
    team_metric = st.selectbox("Select team metric:", ["Total Points", "ROI"])
    team_data = player_df.groupby("Team")[team_metric].mean().sort_values(ascending=False)
    fig = px.bar(team_data, x=team_data.index, y=team_metric, title=f"Teams by Average Player {team_metric}")
    st.plotly_chart(fig)

    # News analysis
    st.subheader("News Analysis")
    news_count = news_df['source_name'].value_counts()
    fig = px.pie(values=news_count.values, names=news_count.index, title="News Sources Distribution")
    st.plotly_chart(fig)

elif page == "Player Scatterplots":
    st.header("Player Scatterplots")

    # Select x and y axes
    x_axis = st.selectbox("Select X-axis:", player_df.select_dtypes(include=['float64', 'int64']).columns)
    y_axis = st.selectbox("Select Y-axis:", player_df.select_dtypes(include=['float64', 'int64']).columns)

    # Create scatterplot
    fig = px.scatter(player_df, x=x_axis, y=y_axis, hover_name="Name", color="Team",
                     title=f"{y_axis} vs {x_axis}")
    st.plotly_chart(fig)

    # Add trend line option
    if st.checkbox("Add trend line"):
        fig = px.scatter(player_df, x=x_axis, y=y_axis, hover_name="Name", color="Team",
                         title=f"{y_axis} vs {x_axis}", trendline="ols")
        st.plotly_chart(fig)

elif page == "Player 3D Plots":
    st.header("Player 3D Plots")

    # Select x, y, and z axes
    numeric_columns = player_df.select_dtypes(include=['float64', 'int64']).columns
    x_axis = st.selectbox("Select X-axis:", numeric_columns, index=0)
    y_axis = st.selectbox("Select Y-axis:", numeric_columns, index=1)
    z_axis = st.selectbox("Select Z-axis:", numeric_columns, index=2)

    # Create 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=player_df[x_axis],
        y=player_df[y_axis],
        z=player_df[z_axis],
        mode='markers',
        marker=dict(
            size=5,
            color=player_df['Team'],
            colorscale='Viridis',
            opacity=0.8
        ),
        text=player_df['Name'],
        hoverinfo='text'
    )])

    fig.update_layout(
        title=f"3D Plot: {x_axis} vs {y_axis} vs {z_axis}",
        scene=dict(
            xaxis_title=x_axis,
            yaxis_title=y_axis,
            zaxis_title=z_axis
        ),
        width=800,
        height=800
    )

    st.plotly_chart(fig)

elif page == "RSS Feeds":
    st.header("RSS Feeds")

    # Display RSS feed data
    st.write("RSS Feed Articles")
    
    # Initialize session state for RSS feed
    if 'rss_index' not in st.session_state:
        st.session_state.rss_index = 0

    # Navigation buttons for RSS feed
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Previous Article"):
            if st.session_state.rss_index > 0:
                st.session_state.rss_index -= 1
    with col3:
        if st.button("Next Article"):
            if st.session_state.rss_index < len(rss_df) - 1:
                st.session_state.rss_index += 1

    # Display the current RSS article
    display_article(rss_df, st.session_state.rss_index)