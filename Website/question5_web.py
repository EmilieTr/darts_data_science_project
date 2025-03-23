import streamlit as st
from .texts import *
from .footer import add_footer
from Visualizations.question_5 import (
    plot_prize_money_and_participants
)

def question5_web():
    st.title("Participants and Price Money")
    st.markdown("---")
    selection = [
    "Participants",
    "Prize Money"
    ]

    # Select multiple tournaments
    selected_vis = st.multiselect(
    "Select Visualization",
    selection,
    default=["Participants", "Prize Money"])
    st.markdown("---")
    
    st.subheader("How does the price money and number of participants of the World Championship vary over time?")
    with st.expander("Explanation"):
        st.write("Hier kommt eine Erklärung der Fragestellung hin.")
    

    
    fig = plot_prize_money_and_participants(selected_vis)
    st.plotly_chart(fig)
    st.text("Hier kommt eine kurze Beschreibung von dem Diagramm hin.")
    with st.expander("Interpretation and critical evaluation"):
        st.write(first_graph_5)

    # Call function to add footer
    add_footer()