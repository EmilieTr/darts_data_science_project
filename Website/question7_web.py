import streamlit as st
from .question7_text import *
from .footer import add_footer
from Visualizations.question_7 import (
    plot_observed_frequencies,
    plot_observed_expected_frequencies,
    plot_conditional_probability
)
    
def question7_web():
    st.title("Host Country vs. Nationality")
    st.markdown("---")
    st.subheader(
        "How does the country a tournament is held in correlate to the success of players?")
    with st.expander("Explanation"):
        st.write(heads_up_7)
    
    
    fig = plot_observed_frequencies()
    st.plotly_chart(fig)
    st.text("There is a significant relationship between the host country and nationality.")
    with st.expander("Interpretation and critical evaluation"):
        st.write(first_graph_7)
    

    fig = plot_observed_expected_frequencies()
    st.plotly_chart(fig)
    st.text("There is no significant relationship between the host country and nationality.")
    with st.expander("Interpretation and critical evaluation"):
        st.write(second_graph_7)
        
    st.image("Visualizations/question_7/map.png")

    # Call function to add footer
    add_footer()