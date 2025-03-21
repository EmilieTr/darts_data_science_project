import streamlit as st
from .texts import *
from .footer import add_footer
from Visualizations.question_2 import plot_winning_averages

def question2_web():
    tournaments = [
        "World Championship",
        "World Matchplay",
        "World Grand Prix",
        "Grand Slam",
        "Players Championship Finals",
        "World Cup",
        "World Series of Darts Finals",
        "European Tour",
        "Players Championship",
        "World Series"
    ]
    
    st.header("2. How do the averages of tournaments vary over time?")
    
    with st.expander("Interpretation"):
        st.write(heads_up_2)

    # Select multiple tournaments
    selected_tournaments = st.multiselect(
        "Select Tournaments",
        tournaments,
        default=["World Championship"]
    )
    
    # Display the selected tournament
    st.subheader(
        "Development of Averages over Time"
    )
    
    # Call the function with the list of selected tournaments
    fig = plot_winning_averages(selected_tournaments)
    st.plotly_chart(fig)

    with st.expander("Interpretation"):
        st.write(first_graph_2)

    # Call function to add footer
    add_footer()