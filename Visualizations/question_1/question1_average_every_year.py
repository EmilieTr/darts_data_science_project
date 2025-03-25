import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_average_every_year(order_of_merit_val):
    """
    Calculate and plot average player statistics across years.
    """
    def convert_name(name):
        """
        Convert names from 'SURNAME, First_name' to 'First_name Surname' format.
        """
        if ", " in name:
            surname, first_name = name.split(", ", 1)  # Divide surname and first name
            surname = surname.capitalize()  # Only the first letter of surname is capitalized
            return f"{first_name} {surname}"
        return name 

    # Load averages
    file_averages = 'Data/Darts_Orakel_Stats/Averages.csv'
    df_averages = pd.read_csv(file_averages)

    # Calculate average stats for each year
    averages_stat = {}
    for year in range(2009, 2025):
        sum = 0
        count = 0

        # Load order of merit for the year
        file = f'Data/order_of_merit/order_of_merit_year_{year}.csv'
        df = pd.read_csv(file)

        # Get top players
        list_best_players = [
            convert_name(name) for name in df['Name'].head(order_of_merit_val)
        ]
        df_averages_year = df_averages[
            (df_averages['Year'] == year) & 
            (df_averages['Player'].isin(list_best_players))
        ]
        
        # Calculate average if data exists
        if not df_averages_year.empty:
            df_averages_year['Stat'] = df_averages_year['Stat'].astype(float)
            for val in df_averages_year['Stat']:
                sum += val
                count += 1
            sum = round((sum / count))
            averages_stat[year] = sum

    # Create line chart
    prism_color = px.colors.qualitative.Prism[0]
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(averages_stat.keys()),
        y=list(averages_stat.values()),
        mode='lines',
        line=dict(color=prism_color, width=2),
        marker=dict(size=6),
        text=[f"{v:.1f}" for v in averages_stat.values()],
        hovertemplate='Year: %{x}<br>Average: %{text}<br><extra></extra>'
    ))

    # Set layout
    fig.update_layout(
        title="Average per Year",
        xaxis_title="Year",
        yaxis_title="Average",
        yaxis_tickformat=".",
        template="plotly_white"
    )
    return fig

# Display diagram
# fig = plot_average_every_year(10)
# fig.show()