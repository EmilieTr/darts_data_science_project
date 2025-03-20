import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_doubles_fields_hits_misses():
    # Read CSV data
    csv_data = "./Data/question 4/question4_doubles.csv"
    df = pd.read_csv(csv_data, header=0)

    # Calculate missed throws (Single, Outside, Other)
    df["Miss"] = df["Single"] + df["Outside"] + df["Other"]

    # Aggregate data by double field
    df_agg = df.groupby("Double")[["Miss", "Hit"]].sum().reset_index()

    # Colors directly from the Prism color palette by index
    prism_colors = px.colors.qualitative.Prism
    color_hit = prism_colors[0]  # Blue
    color_miss = prism_colors[6] # Orange

    # Create a stacked bar chart with Plotly
    fig = go.Figure()

    # Add "Hit" bars
    fig.add_trace(go.Bar(
        x=df_agg["Double"],
        y=df_agg["Hit"],
        name="Hit",
        marker_color=color_hit
    ))

    # Stack "Miss" bars on top of the "Hit" bars
    fig.add_trace(go.Bar(
        x=df_agg["Double"],
        y=df_agg["Miss"],
        name="Miss",
        marker_color=color_miss
    ))

    # Adjust layout
    fig.update_layout(
        barmode="stack",
        title="Stacked Bar Chart of Hits and Misses per Double Field",
        xaxis_title="Double Fields",
        yaxis_title="Number of Throws",
        xaxis=dict(type="category"),  # Set X-axis as categorical (for better presentation)
        legend_title="Outcome"
    )

    return fig
