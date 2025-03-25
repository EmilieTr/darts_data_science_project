import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def plot_distribution_best_double_fields():
    """
    Create a visualization of throws and hits on double fields."
    """
    # Read CSV data
    csv_data = "./Data/question 4/question4_doubles.csv"
    df = pd.read_csv(csv_data)

    # Create a new column with the total number of throws per player
    df["Total"] = df["Hit"] + df["Single"] + df["Outside"] + df["Other"]

    # Find the best double field for each player
    df_max = df.loc[
        df.groupby("Player")["Total"].idxmax(),
        ["Player", "Double", "Hit"]
    ]

    # Count the frequency of each double field
    double_counts = df_max["Double"].value_counts()

    # Group values below 1.5% as "Others"
    total_count = double_counts.sum()
    double_counts_filtered = double_counts[
        double_counts / total_count >= 0.015
    ]
    other_count = double_counts[
        double_counts / total_count < 0.015
    ].sum()

    if other_count > 0:
        double_counts_filtered["Others"] = other_count

    # Count the hits for each double field
    double_counts_hits = df_max.groupby("Double")["Hit"].sum().sort_values(
        ascending=False
    )

    # Group values below 1.5% as "Others"
    total_hits = double_counts_hits.sum()
    double_counts_hits_filtered = double_counts_hits[
        double_counts_hits / total_hits >= 0.015
    ]
    other_hits = double_counts_hits[
        double_counts_hits / total_hits < 0.015
    ].sum()

    if other_hits > 0:
        double_counts_hits_filtered["Others"] = other_hits

    # Colors taken from the Prism color palette
    prism_colors = px.colors.qualitative.Prism
    color_map = {
        double: prism_colors[i % len(prism_colors)]
        for i, double in enumerate(double_counts_filtered.index)
    }

    # Combined figure with subplots
    fig = make_subplots(
        rows=1, cols=2,  # Two charts side by side
        subplot_titles=["Throws on Double Fields", "Hits on Double Fields"],
        specs=[[{"type": "pie"}, {"type": "pie"}]],
        horizontal_spacing=0.25
    )

    # Pie Chart for throws on the double fields (left side)
    fig.add_trace(
        go.Pie(
            labels=[
                f"D{x}" if x != "Others" else x
                for x in double_counts_filtered.index
            ],
            values=double_counts_filtered.values,
            hole=0.3,
            name="Throws",
            marker=dict(
                colors=[
                    color_map.get(x, "gray")
                    for x in double_counts_filtered.index
                ]
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Throws: %{value} (%{percent})<extra></extra>"
            ),
        ),
        row=1,
        col=1
    )

    # Pie Chart for hits on the double fields (right side)
    fig.add_trace(
        go.Pie(
            labels=[
                f"D{x}" if x != "Others" else x
                for x in double_counts_hits_filtered.index
            ],
            values=double_counts_hits_filtered.values,
            hole=0.3,
            name="Hits",
            marker=dict(
                colors=[
                    color_map.get(x, "gray")
                    for x in double_counts_hits_filtered.index
                ]
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Hits: %{value} (%{percent})<extra></extra>"
            ),
        ),
        row=1,
        col=2
    )

    # Layout optimization
    fig.update_layout(
        title_text="Distribution on the Most Popular Double Fields",
        showlegend=True,
        legend=dict(
        x=0.5,
        y=0.5,
        xanchor="center",
        yanchor="middle"),
        width = 600,
        height = 500,
        margin=dict(l=35, r=0, t=0, b=0)
    )

    return fig
