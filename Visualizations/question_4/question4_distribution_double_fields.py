import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def plot_distribution_double_fields():
    """
    Create a visualization of throws and hits on double fields."
    """
    # Read CSV file
    csv_data = "./Data/question 4/question4_doubles.csv"
    df = pd.read_csv(csv_data)

    # Create a new column with total throws per player
    df["Total"] = df["Hit"] + df["Single"] + df["Outside"] + df["Other"]

    # Determine best double field for each player
    df_max = df.loc[
        df.groupby("Double")["Total"].idxmax(),
          ["Double", "Hit"]
    ]

    # Count frequency of each double field
    double_counts = df["Double"].value_counts()

    # Group values below 2% as "Others"
    total_count = double_counts.sum()
    double_counts_filtered = double_counts[
        double_counts / total_count >= 0.02
    ]
    other_count = double_counts[
        double_counts / total_count < 0.02
    ].sum()

    if other_count > 0:
        double_counts_filtered["Others"] = other_count

    # Count hits for each double field
    double_counts_hits = df_max.groupby("Double")["Hit"].sum().sort_values(
        ascending=False
    )


    # Group values below 2% as "Others"
    total_hits = double_counts_hits.sum()
    double_counts_hits_filtered = double_counts_hits[
        double_counts_hits / total_hits >= 0.02
    ]
    other_hits = double_counts_hits[
        double_counts_hits / total_hits < 0.02
    ].sum()

    if other_hits > 0:
        double_counts_hits_filtered["Others"] = other_hits

    # Colors from Prism and Safe color palettes
    prism_colors = px.colors.qualitative.Prism
    for color in px.colors.qualitative.Safe:
        prism_colors.append(color)
    color_map = {
        double: prism_colors[i % len(prism_colors)] 
        for i, double in enumerate(double_counts_filtered.index)
    }

    # Sort double field indices
    double_counts_filtered = double_counts_filtered.sort_index(
        ascending=True, 
        key=lambda x: x.str.extract('(\d+)').astype(float).fillna(0).astype(int).squeeze()
    )
    double_counts_hits_filtered = double_counts_hits_filtered.sort_index(
        ascending=True, 
        key=lambda x: x.str.extract('(\d+)').astype(float).fillna(0).astype(int).squeeze()
    )

    # Move "Others" to end if present
    if 'Others' in double_counts_filtered.index:
        others_value = double_counts_filtered.pop('Others')
        double_counts_filtered['Others'] = others_value

    if 'Others' in double_counts_hits_filtered.index:
        others_value = double_counts_hits_filtered.pop('Others')
        double_counts_hits_filtered['Others'] = others_value

    # Create figure with two subplots
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["Throws on Double Fields", "Hits on Double Fields"],
        specs=[[{"type": "pie"}, {"type": "pie"}]],
        horizontal_spacing=0.3
    )

    # Pie Chart for throws on double fields (left side)
    fig.add_trace(
        go.Pie(
            labels=[f"D{x}" if x != "Others" else x for x in double_counts_filtered.index],
            values=double_counts_filtered.values,
            hole=0.3,
            name="Throws",
            marker=dict(colors=[color_map.get(x, "gray") for x in double_counts_filtered.index]),
            hovertemplate="<b>%{label}</b><br>Throws: %{value} (%{percent})<extra></extra>"
        ),
        row=1, col=1
    )

    # Pie Chart for hits on double fields (right side)
    fig.add_trace(
        go.Pie(
            labels=[f"D{x}" if x != "Others" else x for x in double_counts_hits_filtered.index],
            values=double_counts_hits_filtered.values,
            hole=0.3,
            name="Hits",
            marker=dict(colors=[color_map.get(x, "gray") for x in double_counts_hits_filtered.index]),
            hovertemplate="<b>%{label}</b><br>Hits: %{value} (%{percent})<extra></extra>"
        ),
        row=1, col=2
    )

    # Layout optimization
    fig.update_layout(
        title_text="Distribution of Throws & Hits on Double Fields",
        showlegend=True,
        legend=dict(
        x=0.5,
        y=0.5,
        xanchor="center",
        yanchor="middle"),
        width = 600,
        height = 500
    )

    return fig