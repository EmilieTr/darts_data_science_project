import streamlit as st
from .question2_text import (
    explanation_2,
    first_description_2,
    first_graph_2,
    second_description_2,
    second_graph_2
)
from .footer import add_footer
from Visualizations.question_2 import plot_winning_averages, plot_histogram


def question2_web():
    """
    Render the Streamlit web application for tournament averages visualization.
    """
    tournaments = [
        "World Championship",
        "World Matchplay",
        "World Grand Prix",
        "Grand Slam",
        "Players Championship Finals",
        "World Series of Darts Finals",
        "European Tour",
        "Players Championship"
    ]
    st.title('Averages')
    st.markdown("---")

    # Select multiple tournaments
    selected_tournaments = st.multiselect(
        "Select Tournaments",
        tournaments,
        default=["World Championship", "World Matchplay"]
    )
    
    # Checkbox for additional visualizatoins
    show_regression = st.checkbox("Show regression line", value=True)
    show_std = st.checkbox("Show standard deviation")
    show_all = st.checkbox("Show properties for all tournaments")
    
    st.markdown("---")
    st.subheader("How do the averages of tournaments vary over time?")
    
    with st.expander("Explanation"):
        st.write(explanation_2)

    # Call the winning averages with the list of selected tournaments
    fig = plot_winning_averages(
        selected_tournaments, show_regression, show_std, show_all
        )
    st.plotly_chart(fig)

    st.write(first_description_2)
    with st.expander("Interpretation and critical evaluation"):
        st.write(first_graph_2)

    # Call the histogram with the list of selected tournaments
    fig = plot_histogram(selected_tournaments)
    st.plotly_chart(fig)
    st.write(second_description_2)
    with st.expander("Interpretation and critical evaluation"):
        st.write(second_graph_2)

    # Call function to add footer
    add_footer()