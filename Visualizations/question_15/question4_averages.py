import pandas as pd
import plotly.graph_objects as go

def plot_player_average(player_name):
    # Load the CSV file containing player statistics
    csv_data = "Data/Darts_Orakel_Stats/Averages.csv"
    
    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_data)
    
    # Filter the data for the selected player and 'Averages' category
    df_player = df[(df["Player"] == player_name) & (df["Stat Category"] == "Averages")]
    
    # Check if the player exists in the dataset
    if df_player.empty:
        raise ValueError(f"Player '{player_name}' not found in the data.")
    
    # Sort by year to ensure correct chronological plotting
    df_player = df_player.sort_values(by="Year")

    # Create the line chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_player["Year"],
        y=df_player["Stat"],
        mode="lines+markers",
        name=player_name,
        line=dict(color="blue")
    ))

    # Customize the layout of the chart
    fig.update_layout(
        title=f"Averages Over Time - {player_name}",
        xaxis_title="Year",
        yaxis_title="Average",
        height=500,
        width=800
    )
    
    return fig
