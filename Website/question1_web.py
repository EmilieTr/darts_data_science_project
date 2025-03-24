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
    st.title("Averages of the Best")
    st.markdown("---")
    category = ["Averages", "Checkout Percantages"]
    selected_ranking_position = st.slider("Choose the number of ranking positions", min_value=1, max_value=50, value= 5)
    selected_category = st.selectbox("Select a Category", category)
    if selected_category == "Averages":
        years = [str(i) for i in range(2009, 2025)]

        # Select multiple tournaments
        selected_years = st.multiselect(
            "Select years",
            years,
            default=["2009", "2024"]
        )
    elif selected_category == "Checkout Percentages":
        years = [str(i) for i in range(2012, 2025)]

        # Select multiple tournaments
        selected_years = st.multiselect(
            "Select years",
            years,
            default=["2012", "2024"]
        )
    
    st.markdown("---")
    st.subheader("How does the general performance of players change over "
                "time?")
    
    with st.expander("Explanation"):
        st.write(explanation_1)

    if selected_category == "Averages":

        fig = plot_average_line_chart(selected_ranking_position, selected_years)
        st.plotly_chart(fig)

        st.write(first_description_1)   
        with st.expander("Interpretation and critical evaluation"):
            st.write(first_graph_1)

        fig = plot_average_every_year(selected_ranking_position)
        st.plotly_chart(fig)

        st.write(second_description_1)
        with st.expander("Interpretation and critical evaluation"):
            st.write(second_graph_1)

        st.write(general_1)
        
    elif selected_category == "Checkout Percentage":
        
        fig = plot_checkout_line_chart(selected_ranking_position, selected_years)
        st.plotly_chart(fig)
        
        st.write(third_description_1)
        with st.expander("Interpretation and critical evaluation"):
            st.write(third_graph_1)

        fig = plot_checkout_every_year(selected_ranking_position)
        st.plotly_chart(fig)
        
        st.write(fourth_description_1)
        with st.expander("Interpretation and critical evaluation"):
            st.write(fourth_graph_1)
        
        st.write(general_1)
    
    # Call function to add footer
    add_footer()