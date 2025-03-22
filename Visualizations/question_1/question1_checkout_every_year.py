import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_checkout_every_year(order_of_merit_val):

    # Function to convert names from format "SURNAME, First_name" into "First_name Surname"
    def convert_name(name):
        if ", " in name:
            surname, first_name = name.split(", ", 1)  # Divide surname and first name
            surname = surname.capitalize()  # Only the first letter of surname is capitalized
            return f"{first_name} {surname}"
        return name 
    
    # Load checkout quotes
    file_checkout = 'Data/Darts_Orakel_Stats/Checkout Pcnt.csv'
    df_checkout = pd.read_csv(file_checkout)

    # find for every year (2009-2025) the checkout quote
    averages_stat = {}
    for year in range(2009, 2025):
        sum = 0
        count = 0

        # extracting the requested order of merit ranks in specific years
        file = f'Data/order_of_merit/order_of_merit_year_{year}.csv'
        df = pd.read_csv(file)

        list_best_players = [convert_name(name) for name in df['Name'].head(order_of_merit_val)]
        df_averages_year = df_checkout[(df_checkout['Year'] == year) & (df_checkout['Player'].isin(list_best_players))]
        
        # calculate the average checkout quote
        if not df_averages_year.empty:
            df_averages_year['Stat'] = df_averages_year['Stat'].str.rstrip('%').astype(float) / 100
            for val in df_averages_year['Stat']:
                sum += val
                count += 1
            sum = round((sum / count), 2)
            averages_stat[year] = sum

    # color
    prism_color = px.colors.qualitative.Prism[0]

    # create bar chart 
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=list(averages_stat.keys()),  # years on x-axis
        y=list(averages_stat.values()),  # average checkout quote on y-axis
        text=[f"{v*100:.1f}%" for v in averages_stat.values()],  # Show percentage in the text
        textposition='outside',  # Position text outside the bars
        marker_color=prism_color,  # Bar color
        hovertemplate='Year: %{x}<br>Checkout: %{text}<br><extra></extra>'  # Hover shows year and checkout quote
    ))

    # set layout
    fig.update_layout(
        title="Average Checkout-Quote per Year",
        xaxis_title="Year",
        yaxis_title="Checkout-Quote (%)",
        yaxis_tickformat=".0%",  # Display y-axis as percentages
        template="plotly_white"
    )
    return fig


# Diagramm anzeigen
# fig = plot_checkout_every_year(10)
# fig.show()
