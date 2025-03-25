import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def plot_prize_money_and_participants(selected):
    """
    Create a plot showing prize money and participants over years.
    """
    if not selected:
        # Create empty chart, if selected is empty
        fig = go.Figure()
        fig.add_trace(go.Scatter(
        x=[],  
        y=[],  
        name="Prize Money",
        yaxis="y"
        ))
        fig.add_trace(go.Scatter(
        x=[],  
        y=[],  
        name="Participants",
        yaxis="y2"
        ))

        #  Adjust layout
        fig.update_layout(
            title=(
                "Development of Prize Money and Participants "
                "over the Years (PDC World Championship)"
            ),
            xaxis=dict(
                title="Year"
            ),
            yaxis=dict(
                title="Prize Money (£)",
                side="left"
            ),
            yaxis2=dict(
                title="Participants",
                overlaying="y",
                side="right"
            ),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        return fig
    
    
    def convert_currency(value):
        """
        Convert currency string to float.
        """
        if isinstance(value, str):
            value = value.replace('£', '').replace(',', '')
            return float(value)
        return value


    # Load CSV file
    file = 'Data/question 5/question5.csv'
    df = pd.read_csv(file)

    # Define prize money columns
    columns = [
        'Champion', 'Runner-up', '3d place', '4d place', 'Quarter finalists',
        'Last 16', 'Last 24', 'Last 32', 'Last 64', 'Last 96'
    ]
    labels = [
        '1st', '2nd', '3rd', '4th', 'Quarter finalists', 'Last 16',
        'Last 24', 'Last 32', 'Last 64', 'Last 96'
    ]

    # Convert currency values
    for column in columns:
        df[column] = df[column].apply(convert_currency)
    df['Semi finalists'] = df['Semi finalists'].apply(convert_currency)
    df['Total Prize Pool'] = df['Total Prize Pool'].apply(convert_currency)

    # Fill missing values
    columns_without_3rd_4th = [
        col for col in columns if col not in ['3d place', '4d place']
    ]
    df[columns_without_3rd_4th] = df[columns_without_3rd_4th].fillna(0)
    df['3d place'].fillna(df['Semi finalists'], inplace=True)
    df['4d place'].fillna(df['Semi finalists'], inplace=True)

    # Multiply specific columns by respective factors
    df['Quarter finalists'] *= 4
    df['Last 16'] *= 8
    df['Last 24'] *= 8
    df['Last 32'] *= 32
    df['Last 64'] *= 32
    df['Last 96'] *= 32
    
    # Group participant data
    participants_per_year = df.groupby('Year')['Participants'].mean()

    # Create Plotly figure
    fig = go.Figure()

    # Colors of Prism Color Scheme
    prism_colors = px.colors.qualitative.Prism
    color_count = len(columns) + 1
    prism_colors = prism_colors[1:color_count]

    if "Prize Money" in selected:
        # Stacked bar chart for prize money
        bottom_values = [0] * len(df['Year'])

        for i, (column, label) in enumerate(zip(columns, labels)):
            fig.add_trace(go.Bar(
                x=df['Year'],
                y=df[column],
                name=label,
                marker=dict(
                    color=prism_colors[i % len(prism_colors)],
                    line=dict(width=0)
                ),
                hovertemplate=(
                    'Position: %{data.name}<br>'
                    'Year: %{x}<br>'
                    'Prize Money: £%{y:.0f}<br><extra></extra>'
                )
            ))
            bottom_values = [sum(x) for x in zip(bottom_values, df[column])]


    if "Participants" in selected:
        # Line plot for participants
        fig.add_trace(go.Scatter(
            x=participants_per_year.index,
            y=participants_per_year.values,
            mode='lines',
            name='Participants',
            yaxis='y2',
            line=dict(color='red', width=2),
            hovertemplate=(
                'Year: %{x}<br>'
                'Participants: %{y}<br><extra></extra>'
            )
        ))

    # Determine title
    title = "Development of "
    if "Prize Money" in selected and "Participants" in selected:
        title += "Prize Money and Participants"
    elif "Prize Money" in selected:
        title += "Prize Money"
    elif "Participants" in selected:
        title += "Participants"
    title += " over the Years (PDC World Championship)"

    #  Adjust layout
    fig.update_layout(
        title=title,
        xaxis=dict(
            title="Year",
            showgrid=False
        ),
        yaxis=dict(
            title="Prize Money (£)",
            side="left",
            showgrid=False
        ),
        yaxis2=dict(
            title="Participants",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        barmode="stack",
        legend=dict(
            x=1.2,
            y=1
        ),
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return fig

# fig = plot_prize_money_and_participants(['Prize Money', 'Participants'])
# fig.show()
