import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import scipy.stats as stats

def plot_histogram(column):
    """
    Create a histogram for the specified column 
    with a normal distribution curve overlay.
    
    :param column: The column for which the histogram is created
    :return: Plotly Figure object
    """
    # Load CSV file
    df = pd.read_csv("Visualizations/question_9/180_stats.csv")
    
    # Clean data
    df_cleaned = df.dropna(subset=[column])

    # Calculate the mean and standard deviation
    mu, sigma = df_cleaned[column].mean(), df_cleaned[column].std()

    # Create histogram data with fewer bins
    nbins = 10
    hist_data = np.histogram(df_cleaned[column], bins=nbins)
    bin_edges = hist_data[1]
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Generate normal distribution curve
    x_values = np.linspace(
        min(df_cleaned[column]), 
        max(df_cleaned[column]), 
        100
    )
    y_values = stats.norm.pdf(
        x_values, 
        mu, 
        sigma
    ) * len(df_cleaned) * (bin_edges[1] - bin_edges[0])

    prism_colors = px.colors.qualitative.Prism

    # Create the Plotly figure
    fig = go.Figure()

    # Add the histogram to the figure
    fig.add_trace(go.Bar(
        x=bin_centers, 
        y=hist_data[0], 
        name=f"Histogram of {column}", 
        marker=dict(color=prism_colors[1], opacity=0.7),
    ))

    # Add the normal distribution curve to the figure
    fig.add_trace(go.Scatter(
        x=x_values, 
        y=y_values, 
        mode="lines", 
        line=dict(color=prism_colors[7], width=2), 
        name="Normal Distribution"
    ))

    # Update layout settings
    fig.update_layout(
        title=f"Histogram of {column} with Normal Distribution",
        xaxis_title=column,
        yaxis_title="Frequency",
        template="plotly_dark",
        bargap=0.1,
        hovermode="x unified"
    )

    return fig
