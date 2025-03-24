import streamlit as st
from .texts import *
from .footer import add_footer
from Visualizations.question_2 import plot_winning_averages
from Visualizations.question_2 import plot_histogram

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
    st.title('Averages')
    
    st.markdown("---")
    # Select multiple tournaments
    selected_tournaments = st.multiselect(
        "Select Tournaments",
        tournaments,
        default=["World Championship"]
    )
    
    # Checkbox für Regression
    show_regression = st.checkbox("Show regression line for average")

    # Checkbox für Regression
    show_std = st.checkbox("Show standard deviation for average")
    
    st.markdown("---")

    # Display the selected tournament
    st.subheader("How do the averages of tournaments vary over time?")
    
    with st.expander("Explanation"):
        st.write(explanation_2)

    # Call the function with the list of selected tournaments
    fig = plot_winning_averages(selected_tournaments, show_regression, show_std)
    st.plotly_chart(fig)

    st.text(first_description_2)
    with st.expander("Interpretation and critical evaluation"):
        st.write(first_graph_2)

    # Call the function with the list of selected tournaments
    fig = plot_histogram(selected_tournaments)
    st.plotly_chart(fig)
    st.text("Hier kommt eine kurze Beschreibung von dem Diagramm hin.")
    with st.expander("Interpretation and critical evaluation"):
        st.write(second_graph_2)

    # Call function to add footer
    add_footer()