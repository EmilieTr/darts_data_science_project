import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_average_every_year(order_of_merit_val):

    # Function to convert names from format "SURNAME, First_name" into "First_name Surname"
    def convert_name(name):
        if ", " in name:
            surname, first_name = name.split(", ", 1)  # Divide surname and first name
            surname = surname.capitalize()  # Only the first letter of surname is capitalized
            return f"{first_name} {surname}"
        return name 

    # Load averages
    file_averages = 'Data/Darts_Orakel_Stats/Averages.csv'
    df_averages = pd.read_csv(file_averages)

    # find for every year (2009-2025) the average Stats
    averages_stat = {}
    for year in range(2009, 2025):
        sum = 0
        count = 0

        # extracting the requested order of merit ranks in specific years
        file = f'Data/order_of_merit/order_of_merit_year_{year}.csv'
        df = pd.read_csv(file)

        list_best_players = [convert_name(name) for name in df['Name'].head(order_of_merit_val)]
        df_averages_year = df_averages[(df_averages['Year'] == year) & (df_averages['Player'].isin(list_best_players))]
        
        # calculate the average
        if not df_averages_year.empty:
            df_averages_year['Stat'] = df_averages_year['Stat'].astype(float)
            for val in df_averages_year['Stat']:
                sum += val
                count += 1
            sum = round((sum / count))
            averages_stat[year] = sum

    # color
    prism_color = px.colors.qualitative.Prism[0]

    # create bar chart 
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(averages_stat.keys()),  # years on x-axis
        y=list(averages_stat.values()),  # averages on y-axis
        text=[f"{v:.1f}" for v in averages_stat.values()], 
        textposition='outside', 
        marker_color=prism_color
    ))

    # set layout
    fig.update_layout(
        title="Average per year",
        xaxis_title="year",
        yaxis_title="average",
        yaxis_tickformat=".",
        template="plotly_white"
    )
    return fig


# Diagramm anzeigen
#fig = plot_average_every_year(10)
#fig.show()