import pandas as pd
import plotly.graph_objects as go
import plotly.express as px  # For colors (px.colors.qualitative.Paired)
from plotly.subplots import make_subplots  # For multiple plots in a single figure

def plot_double_fields_player(player):
    """
    This function creates a chart that shows the number of throws and the double quota of a player
    over the years for various doubles fields.
    
    Parameters:
    player (str): The name of the player whose data should be visualized.
    """

    # Read CSV data
    csv_data = "./Data/question 4/question4_doubles.csv"
    df = pd.read_csv(csv_data)

    # Filter for the specific player (Replace 'Player S' with the actual player's name)
    df_player = df[df["Player"] == player]

    # Filter: Keep only values where Hits >= 20 (to exclude low-value throws)
    df_player = df_player[df_player["Hit"] >= 20]

    # Calculate total throws (Hit + Single + Outside + Other)
    df_player["Total"] = df_player["Hit"] + df_player["Single"] + df_player["Outside"] + df_player["Other"]

    # Calculate double quota: Hits / Total throws
    df_player["Double quota"] = df_player["Hit"] / df_player["Total"]

    # Calculate the average hits per double field
    mean_hits = df_player.groupby("Double")["Hit"].mean()

    # Filter out doubles with an average of less than 120 hits
    if player == "Luke Littler":
        min_hits = 40  # For Luke Littler, the threshold is 40 hits
    else:
        min_hits = 120  # Default threshold for other players is 120 hits
    top_doubles = mean_hits[mean_hits >= min_hits].index  # List of relevant doubles fields

    # Assign colors to doubles fields (using the Plotly Prism palette)
    colors = px.colors.qualitative.Prism
    color_map = {double: colors[i % len(colors)] for i, double in enumerate(sorted(df_player["Double"].unique()))}

    # Create a figure with two subplots: one for throws and one for double quota
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Throws on Double Fields", "Double Quota"))

    # LEFT PLOT: Number of throws over the years (ALL DOUBLE FIELDS)
    for double_value in sorted(df_player["Double"].unique()):
        player_data = df_player[df_player["Double"] == double_value]
        fig.add_trace(
            go.Scatter(x=player_data["Year"], y=player_data["Total"], mode="lines", name=f'D {double_value}', line=dict(color=color_map[double_value])),
            row=1, col=1
        )

    # RIGHT PLOT: Double quota over the years (ONLY TOP DOUBLES FIELDS)
    for double_value in top_doubles:
        player_data = df_player[df_player["Double"] == double_value]
        fig.add_trace(
            go.Scatter(x=player_data["Year"], y=player_data["Double quota"], mode="lines", name=f'D {double_value}', line=dict(color=color_map[double_value])),
            row=1, col=2
        )

    # Adjust layout
    fig.update_layout(
        title=f"Player: {player}",
        xaxis_title="Year",
        yaxis_title="Number of Throws",
        xaxis2_title="Year",
        yaxis2_title="Double Quota",
        showlegend=True,
        height=600,
        width=1200,
    )

    # Return the generated figure
    return fig
