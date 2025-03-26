import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_checkout_every_year(order_of_merit_val):
    """
    Calculate and plot average checkout percentages across years.
    """
    def convert_name(name):
        """
        Convert names from 'SURNAME, First_name' to 'First_name Surname' format."
        """
        if ", " in name:
            surname, first_name = name.split(", ", 1)
            surname = surname.capitalize()
            return f"{first_name} {surname}"
        return name 
    
    # Load checkout percentages
    file_checkout = 'Data/Darts_Orakel_Stats/Checkout Pcnt.csv'
    df_checkout = pd.read_csv(file_checkout)

    # Calculate checkout percentages for each year
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
        df_averages_year = df_checkout[
            (df_checkout['Year'] == year) & 
            (df_checkout['Player'].isin(list_best_players))
        ]
        
        # calculate the average checkout quote
        if not df_averages_year.empty:
            df_averages_year['Stat'] = (
                df_averages_year['Stat'].str.rstrip('%').astype(float) / 100
            )
            for val in df_averages_year['Stat']:
                sum += val
                count += 1
            sum = round((sum / count), 2)
            averages_stat[year] = sum

    # Color
    prism_color = px.colors.qualitative.Prism[0]

    # Create line chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(averages_stat.keys()),
        y=list(averages_stat.values()),
        mode='lines',
        line=dict(color=prism_color, width=2),
        marker=dict(size=6),
        text=[f"{v*100:.1f}%" for v in averages_stat.values()],
        hovertemplate='Year: %{x}<br>Checkout Percentage: %{text}<br><extra></extra>'
    ))

    # Set layout
    fig.update_layout(
        title="Average Checkout Percentage per Year",
        xaxis_title="Year",
        yaxis_title="Checkout Percentage (%)",
        yaxis_tickformat=".0%",
        template="plotly_white"
    )
    return fig


# Display graph
# fig = plot_checkout_every_year(10)
# fig.show()