import streamlit as st
from .texts import *
from .footer import add_footer
from Visualizations.question_5 import (
    plot_prize_money_and_participants
)

def question5_web():

    st.header("5. How does the price money and number of participants vary "
            "over time?")

    selection = [
    "Participants",
    "Prize Money"
    ]

    # Select multiple tournaments
    selected_vis = st.multiselect(
    "Select Visualization",
    selection,
    default=["Participants", "Prize Money"]
    )

    st.subheader(
    "Participants and Price Money of the World Championships "
    "over the Years"
    )
    fig = plot_prize_money_and_participants(selected_vis)
    st.plotly_chart(fig)

    with st.expander("Interpretation"):
        st.write(first_graph_5)

    # Call function to add footer
    add_footer()