import pandas as pd
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stats
import plotly.express as px

def plot_histogram(selected_tournaments):
    """
    Generate a histogram of average scores with a normal distribution curve."
    """
    if not selected_tournaments:
        fig = go.Figure()
        fig.update_layout(
        title="Histogram of Average Scores with Normal Distribution",
        xaxis_title="Average Score",
        yaxis_title="Frequency",
        legend_title="Legend",
        hovermode="closest"
        )

        return fig
    
    # Load CSV file
    file = 'Data/question 2/question2.csv'
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()

    # Filter data for valid averages
    df_cleaned = df.dropna(subset=['Average'])
    df_cleaned = df_cleaned[df_cleaned['Average'] >= 10]
    df_selected = df_cleaned[
        df_cleaned['Tournament'].isin(selected_tournaments)
    ]

    # Calculate normal distribution parameters
    mu, sigma = df_selected['Average'].mean(), df_selected['Average'].std()

    # Create histogram
    hist_data = np.histogram(df_selected['Average'], bins=20)
    bin_edges = hist_data[1]
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Generate normal distribution curve
    x_values = np.linspace(
        min(df_selected['Average']),
        max(df_selected['Average']),
        100
    )
    y_values = stats.norm.pdf(x_values, mu, sigma) * len(df_selected) * (
        bin_edges[1] - bin_edges[0]
    )

<<<<<<< HEAD
    prism_colors = px.colors.qualitative.Prism

    # Erstellen der Plotly-Figur
=======
    # Create Plotly figure
>>>>>>> 74a7d494695b20e7c45b50f0a13525ee7b981fc4
    fig = go.Figure()

    # Add histogram
    fig.add_trace(go.Bar(
<<<<<<< HEAD
        x=bin_centers, 
        y=hist_data[0], 
        name="Histogram", 
        marker=dict(color=prism_colors[1], opacity=0.7),
        hovertemplate='Average Score: %{x}<br>Frequency: %{y}<extra></extra>',  # Nur X- und Y-Wert anzeigen
=======
        x=bin_centers,
        y=hist_data[0],
        name="Histogram",
        marker=dict(color='lightblue', opacity=0.7),
        hovertemplate='Average Score: %{x}<br>Frequency: %{y}<extra></extra>',
>>>>>>> 74a7d494695b20e7c45b50f0a13525ee7b981fc4
        hoverlabel=dict(namelength=-1)
    ))

    # Add normal distribution curve
    fig.add_trace(go.Scatter(
        x=x_values, 
        y=y_values, 
        mode="lines", 
        line=dict(color=prism_colors[7], width=2), 
        name="Normal Distribution",
        hovertemplate='Normal Distribution: %{y}<extra></extra>'
    ))

    # Adjust Layout
    fig.update_layout(
        title="Histogram of Average Scores with Normal Distribution",
        xaxis_title="Average Score",
        yaxis_title="Frequency",
        template="plotly_dark",
        bargap=0.1,
        hovermode="closest"
    )

    return fig
