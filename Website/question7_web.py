import streamlit as st
from .texts import *
from .footer import add_footer
from Visualizations.question_7 import (
    plot_observed_frequencies,
    plot_observed_expected_frequencies,
    plot_conditional_probability
)
    
def question7_web():
    st.header(
        "7. How does the country a tournament is held in correlate "
        "to the success of players?"
    )

    with st.expander("Interpretation"):
        st.write(heads_up_7)
    
    st.subheader("Observed Frequencies")
    fig = plot_observed_frequencies()
    st.plotly_chart(fig)

    with st.expander("Interpretation"):
        st.write(first_graph_7)
    
    st.subheader("Difference between Observed and Expected Frequencies")
    fig = plot_observed_expected_frequencies()
    st.plotly_chart(fig)

    with st.expander("Interpretation"):
        st.write(second_graph_7)
        
    st.image("Visualizations/question_7/map.png")

    with st.expander("Interpretation"):
        st.write(fourth_graph_7)

    # Call function to add footer
    add_footer()