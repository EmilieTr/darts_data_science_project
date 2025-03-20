import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_double_fields_player_combined(player, double):
    # Load CSV data
    csv_data_checkout = "./Data/question 4/question4_doubles.csv"
    df_checkout = pd.read_csv(csv_data_checkout)

    # Filter data for the selected player and double field
    double = int(double[1:])  # Remove the 'D' from the double field (e.g., "D20" -> 20)
    df_checkout = df_checkout[(df_checkout["Player"] == player) & (df_checkout["Double"] == double)]

    # Calculate total throws (Hit + Single + Outside + Other)
    df_checkout["Total"] = df_checkout["Hit"] + df_checkout["Single"] + df_checkout["Outside"] + df_checkout["Other"]

    # Calculate double quota (Hit / Total)
    df_checkout["Double Quota"] = df_checkout["Hit"] / df_checkout["Total"]

    # Use colors from the Plotly Express Prism color palette
    prism_colors = px.colors.qualitative.Prism
    color_throws = prism_colors[0]  # First color from the Prism palette
    color_quota = prism_colors[6]   # Fourth color from the Prism palette

    # Create an interactive plot
    fig = go.Figure()

    # Line plot for the number of throws (left y-axis)
    fig.add_trace(go.Scatter(
        x=df_checkout["Year"], 
        y=df_checkout["Total"], 
        mode="lines+markers", 
        name="Number of Throws",
        yaxis="y1",
        line=dict(color=color_throws)
    ))

    # Line plot for the double quota (right y-axis)
    fig.add_trace(go.Scatter(
        x=df_checkout["Year"], 
        y=df_checkout["Double Quota"], 
        mode="lines+markers", 
        name="Double Quota",
        yaxis="y2",
        line=dict(color=color_quota, dash="dash")
    ))

    # Update layout
    fig.update_layout(
        title=f"Number of Throws and Double Quota from {player} on D {double}",
        xaxis=dict(
            title="Year",
            showgrid=False  # Remove horizontal gridlines for the x-axis
        ),
        yaxis=dict(
            title="Number of Throws",
            tickfont=dict(color=color_throws),
            showgrid=False  # Remove horizontal gridlines for the left y-axis
        ),
        yaxis2=dict(
            title="Double Quota",
            tickfont=dict(color=color_quota),
            overlaying="y",
            side="right",
            showgrid=False  # Remove horizontal gridlines for the right y-axis
        ),
        legend=dict(x=0.01, y=0.99),
        height=600,
        width=1000
    )

    return fig
