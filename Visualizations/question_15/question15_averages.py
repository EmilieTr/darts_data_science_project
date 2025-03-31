import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_player_average(player_name):
    """
    Plot the average performance of a player over time."
    """
    csv_data = "Data/darts_orakel_stats/player_averages.csv"
    
    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_data)
    
    # Filter the data for the selected player and 'Averages' category
    df_player = df[
        (df["Player"] == player_name) & (df["Stat Category"] == "Averages")
    ]
    
    # Check if the player exists in the dataset
    if df_player.empty:
        raise ValueError(f"Player '{player_name}' not found in the data.")
    
    # Sort by year to ensure correct chronological plotting
    df_player = df_player.sort_values(by="Year")

    # Create a color scale from the Prism palette based on the years
    color = px.colors.qualitative.Prism[8]

    # Create the line chart with colors based on year
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_player["Year"],
        y=df_player["Stat"],
        mode="lines",
        name=player_name,
        line=dict(color=color),
        marker=dict(color=color),
        hovertemplate='<br>Year: %{x}<br>Average: %{y:.2f}<br><extra></extra>',
        text=[player_name] * len(df_player)
    ))

    # Customize the layout of the chart
    fig.update_layout(
        title=f"Averages - {player_name}",
        xaxis_title="Year",
        yaxis_title="Average",
        height=500,
        width=800
    )
    
    return fig
