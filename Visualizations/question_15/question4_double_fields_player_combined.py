import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_double_fields_player_combined(player, double):
    """
    Create a combined visualization of throws and checkout percentage."
    """
    # Load CSV file
    csv_data_checkout = "./Data/doubles_checkout.csv"
    df_checkout = pd.read_csv(csv_data_checkout)

    # Prepare data
    double = int(double[1:])  # Convert 'D20' to 20
    df_checkout = df_checkout[
        (df_checkout["Player"] == player) & (df_checkout["Double"] == double)
    ]

    # Calculate total throws (Hit + Single + Outside + Other)
    df_checkout["Total"] = (
        df_checkout["Hit"] +
        df_checkout["Single"] +
        df_checkout["Outside"] +
        df_checkout["Other"]
    )
    df_checkout["Checkout Percentage"] = df_checkout["Hit"] / df_checkout["Total"]

    # Use colors from the Plotly Express Prism color palette
    prism_colors = px.colors.qualitative.Prism
    color_throws = prism_colors[0]
    color_quota = prism_colors[6]

    # Create an interactive plot
    fig = go.Figure()

    # Line plot for the number of throws (left y-axis)
    fig.add_trace(go.Scatter(
        x=df_checkout["Year"], 
        y=df_checkout["Total"], 
        mode="lines", 
        name="Number of Throws",
        yaxis="y1",
        line=dict(color=color_throws),
        hovertemplate=(
            '<b>%{text}</b><br>Year: %{x}<br>Throws: %{y}<br><extra></extra>'
        ),
        text=[f'D{double}'] * len(df_checkout)
    ))

    # Line plot for the double percentage (right y-axis)
    fig.add_trace(go.Scatter(
        x=df_checkout["Year"], 
        y=df_checkout["Checkout Percentage"], 
        mode="lines", 
        name="Checkout Percentage",
        yaxis="y2",
        line=dict(color=color_quota, dash="dash"),
        hovertemplate=(
            '<b>%{text}</b><br>Year: %{x}<br>'
            'Checkout Percentage: %{y:.2f}<br><extra></extra>'
        ),
        text=[f'D{double}'] * len(df_checkout)
    ))

    # Update layout
    fig.update_layout(
        title=f"Number of Throws and Checkout Percentage of D{double} - {player}",
        xaxis=dict(
            title="Year",
            showgrid=False
        ),
        yaxis=dict(
            title="Number of Throws",
            tickfont=dict(color=color_throws),
            showgrid=False
        ),
        yaxis2=dict(
            title="Checkout Percentage",
            tickfont=dict(color=color_quota),
            overlaying="y",
            side="right",
            showgrid=False
        ),
        legend=dict(x=1.1, y=0.99),
        height=600,
        width=1000
    )

    return fig
