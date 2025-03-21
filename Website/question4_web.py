import streamlit as st
from .texts import *
from .footer import add_footer
from Visualizations.question_4 import (
    plot_distribution_double_fields,
    plot_distribution_best_double_fields
)

def question4_web():    
    st.header(
        "4. What are most popular double fields and their "
        "corresponding checkout quotes?"
    )
    
    st.subheader("Distribution of Throws and Hits on Double Fields")
    fig = plot_distribution_double_fields()
    st.plotly_chart(fig)

    with st.expander("Interpretation"):
        st.write(first_graph_4)
    
    st.subheader(
        "Distribution of Throws and Hits on the Best Double Fields "
        "per Player"
    )
    fig = plot_distribution_best_double_fields()
    st.plotly_chart(fig)

    with st.expander("Interpretation"):
        st.write(second_graph_4)

    # Call function to add footer
    add_footer()