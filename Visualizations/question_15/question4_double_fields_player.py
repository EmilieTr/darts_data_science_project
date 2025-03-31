import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def plot_double_fields_player(player):
    """
    Create a chart showing a player's throws and checkout percentage over years.
    """
    # Read CSV data
    csv_data = "./Data/doubles_checkout.csv"
    df = pd.read_csv(csv_data)

    # Filter for the specific player
    df_player = df[df["Player"] == player]

    # Filter: Keep only values where Hits >= 20
    df_player = df_player[df_player["Hit"] >= 20]

    # Calculate total throws
    df_player["Total"] = (
        df_player["Hit"] +
        df_player["Single"] +
        df_player["Outside"] +
        df_player["Other"]
    )

    # Calculate checkout percentage
    df_player["Checkout Percentage"] = df_player["Hit"] / df_player["Total"]

    # Calculate the average hits per double field
    mean_hits = df_player.groupby("Double")["Hit"].mean()

    # Set minimum hits threshold based on player
    if player == "Luke Littler":
        min_hits = 40
    else:
        min_hits = 120
    top_doubles = mean_hits[mean_hits >= min_hits].index

    # Assign colors to doubles fields
    colors = px.colors.qualitative.Prism[:9]
    for color in px.colors.qualitative.Safe:
        colors.append(color)
    del colors[12]
    color_map = {
        double: colors[i % len(colors)]
        for i, double in enumerate(sorted(df_player["Double"].unique()))
    }

    # Create a figure with two subplots
    fig = make_subplots(
        rows=1, 
        cols=2, 
        subplot_titles=("Throws on Double Fields", "Checkout Percentage"),
        horizontal_spacing=0.2 
    )

    # LEFT PLOT: Number of throws over the years
    for double_value in sorted(df_player["Double"].unique()):
        player_data = df_player[df_player["Double"] == double_value]
        fig.add_trace(
            go.Scatter(
                x=player_data["Year"], 
                y=player_data["Total"], 
                mode="lines", 
                name=f'D{double_value}', 
                line=dict(color=color_map[double_value]),
                hovertemplate=(
                    '<b>%{text}</b><br>Year: %{x}<br>Throws: %{y}<br><extra></extra>'
                ),
                text=[f'D{double_value}'] * len(player_data)
            ),
            row=1, col=1
        )

    # RIGHT PLOT: Checkout Percentage over the years
    for double_value in sorted(top_doubles):
        player_data = df_player[df_player["Double"] == double_value]
        fig.add_trace(
            go.Scatter(
                x=player_data["Year"], 
                y=player_data["Checkout Percentage"], 
                mode="lines", 
                name=f'D{double_value}', 
                line=dict(color=color_map[double_value]),
                hovertemplate=(
                    '<b>%{text}</b><br>Year: %{x}<br>'
                    'Checkout Percentage: %{y:.2f}<br><extra></extra>'
                ),
                text=[f'D{double_value}'] * len(player_data),
                showlegend=False
            ),
            row=1, col=2
        )

    # Adjust layout
    fig.update_layout(
        title=f"Throws on Double Fields and Checkout Percentage - {player}",
        xaxis_title="Year",
        yaxis_title="Number of Throws",
        xaxis2_title="Year",
        yaxis2_title="Checkout Percentage",
        showlegend=True,
        height=600,
        width=1200,
    )

    return fig
