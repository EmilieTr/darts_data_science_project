import streamlit as st
from .texts import *
from .footer import add_footer
from Visualizations.question_6 import (
    plot_ranking_age,
    plot_ranking_nationality,
    plot_ranking_handedness
)

def question6_web():    
    st.header("6. How does age, nationality and handiness effects "
                "the rankings?")
    
    # Erstelle einen Slider von 0 bis 50
    selected_ranking_position= st.slider("Choose the number of ranking positions", min_value=1, max_value=50)
    variant = st.radio("Choose an Option", ("absolute values", "relative values"))
    
    if variant == "absolute values":
        variant = 1
    else:
        variant = 0
    
    st.subheader("Age Participants Over the Years")
    fig, _ = plot_ranking_age(selected_ranking_position, variant)
    st.plotly_chart(fig)

    with st.expander("Interpretation"):
        st.write(first_graph_6)
    
    st.subheader("Nationality Participants Over the Years")
    fig, _ = plot_ranking_nationality(selected_ranking_position, variant)
    st.plotly_chart(fig)

    with st.expander("Interpretation"):
        st.write(second_graph_6)
    
    st.subheader("Handedness Participants Over the Years")
    fig, _ = plot_ranking_handedness(selected_ranking_position, variant)
    st.plotly_chart(fig)

    with st.expander("Interpretation"):
        st.write(third_graph_6)

    # Call function to add footer
    add_footer()