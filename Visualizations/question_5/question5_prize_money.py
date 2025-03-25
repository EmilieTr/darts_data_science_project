import pandas as pd
import plotly.express as px

def plot_prize_money():
    # Function to convert currency strings to float
    def convert_currency(value):
        """
        Convert currency string to float."
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

    # Melt the DataFrame for the area chart
    df_melted = df.melt(
        id_vars='Year',
        value_vars=columns,
        var_name='Position',
        value_name='Prize Money'
    )

    # Map the columns to more readable labels
    df_melted['Position'] = df_melted['Position'].replace(
        dict(zip(columns, labels))
    )

    # Ensure the order of the categories (Last 96 to 1st)
    df_melted['Position'] = pd.Categorical(
        df_melted['Position'],
        categories=labels[::-1],
        ordered=True
    )

    # Create overlapping area chart
    fig = px.line(
        df_melted,
        x='Year',
        y='Prize Money',
        color='Position',
        title=(
            'Distribution of Prize Money over the Years '
            '(PDC World Championship)'
        ),
        color_discrete_sequence=px.colors.qualitative.Prism[1:],
        hover_data={'Prize Money': ':.0f'},
        line_group='Position'
    )

    # Ensure full opacity and remove transparency
    fig.update_traces(mode='lines', fill='tozeroy', opacity=1.0, fillcolor=None)

    # Customize layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Prize Money (£)',
        legend_title='Position',
        margin=dict(l=50, r=50, t=50, b=50),
        plot_bgcolor='white'
    )

    return fig

# fig = plot_prize_money()
# fig.show()
