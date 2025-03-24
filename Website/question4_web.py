import streamlit as st
from .question4_text import *
from .footer import add_footer
from Visualizations.question_4 import (
    plot_distribution_double_fields,
    plot_distribution_best_double_fields
)

def question4_web(): 
    st.title("Popular Douple Fields")   
    st.markdown("---")
    st.subheader("What are most popular double fields and their corresponding checkout quotes?")
    with st.expander("Explanation"):
        st.write("Explanation")

    fig = plot_distribution_double_fields()
    st.plotly_chart(fig)
    st.text("kurze Beschreibung was man im Diagramm für Ergebnisse sieht")
    with st.expander("Interpretation and critical evaluation"):
        st.write(first_graph_4)
    
    fig = plot_distribution_best_double_fields()
    st.plotly_chart(fig)
    st.text("kurze Beschreibung was man im Diagramm für Ergebnisse sieht")
    with st.expander("Interpretation and critical evaluation"):
        st.write(second_graph_4)

    # Call function to add footer
    add_footer()