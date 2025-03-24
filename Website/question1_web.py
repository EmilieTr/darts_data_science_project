import streamlit as st
from .question1_text import *
from .footer import add_footer
from Visualizations.question_1 import (
    plot_checkout_every_year,
    plot_checkout_line_chart,
    plot_average_every_year,
    plot_average_line_chart
)

def question1_web():    
    st.header("1. How does the general performance of players change over "
                "time?")
    
    category = ["Averages", "Checkout Quota"]
    selected_ranking_position = st.slider("Choose the number of ranking positions", min_value=2, max_value=33)
    selected_category = st.selectbox("Select a Category", category)
    
    if selected_category == "Averages":
        years = [str(i) for i in range(2009, 2025)]

        # Select multiple tournaments
        selected_years = st.multiselect(
            "Select years",
            years,
            default=["2009", "2024"]
        )
    
        st.subheader("Development of Averages in 2009 vs. 2024")
        fig = plot_average_line_chart(selected_ranking_position, selected_years)
        st.plotly_chart(fig)

        with st.expander("Interpretation"):
            st.write(first_graph_1)
        
        st.subheader("Development of Averages over the Years")
        fig = plot_average_every_year(selected_ranking_position)
        st.plotly_chart(fig)

        with st.expander("Interpretation"):
            st.write(second_graph_1)
        
    elif selected_category == "Checkout Quota":
        years = [str(i) for i in range(2012, 2025)]

        # Select multiple tournaments
        selected_years = st.multiselect(
            "Select years",
            years,
            default=["2012", "2024"]
        )
        
        st.subheader("Development of Checkouts in 2012 vs. 2024")
        fig = plot_checkout_line_chart(selected_ranking_position, selected_years)
        st.plotly_chart(fig)
        
        st.subheader("Development of Checkouts over the Years")
        fig = plot_checkout_every_year(selected_ranking_position)
        st.plotly_chart(fig)

        with st.expander("Interpretation"):
            st.write(third_graph_1)
    
        with st.expander("General Interpretation"):
            st.write(interpretation_1)   
    
    # Call function to add footer
    add_footer()