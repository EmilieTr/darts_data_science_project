import streamlit as st
from .question4_text import *
from .footer import add_footer
from Visualizations.question_4 import (
    plot_distribution_double_fields,
    plot_distribution_best_double_fields
)


def question4_web(): 
    st.title("Popular Double Fields")   
    st.markdown("---")
    st.subheader(
        "What are the most popular double fields and their "
        "corresponding checkout percentages?"
    )

    with st.expander("Explanation"):
        st.write(explanation_4)

    fig = plot_distribution_double_fields()
    st.plotly_chart(fig)
    st.write(first_description_4)

    with st.expander("Interpretation and critical evaluation"):
        st.write(first_graph_4)
    
    fig = plot_distribution_best_double_fields()
    st.plotly_chart(fig)
    st.write(second_description_4)
    
    with st.expander("Interpretation and critical evaluation"):
        st.write(second_graph_4)

    # Call function to add footer
    add_footer()