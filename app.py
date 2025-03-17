import streamlit as st
import pandas as pd
from Visualizations.question_1 import plot_checkout_every_year, plot_average_2009_2024, plot_average_every_year, plot_checkout_2012_2024
from Visualizations.question_2 import plot_winning_averages
from Visualizations.question_4 import plot_double_fields_player_combined, plot_distribution_double_fields, plot_double_fields_player, plot_doubles_fields_hits_misses
from Visualizations.question_5 import plot_price_money_and_participants, plot_participants, plot_price_money
#from Visualizations.question_6 import question_1
from Visualizations.question_7 import plot_observed_frequencies, plot_observed_expected_frequencies, plot_conditional_probability
from Visualizations.question_8 import plot_comparison_single_team
#from Visualizations.question_9 import question_1

# Sidebar für Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Development of Tournaments", "Strategies and Tactics", "Players"])

# Seite wechseln  
if page == "Development of Tournaments":
    subpage = st.sidebar.radio("Development of Tournaments", ["Development of Tournaments", "Price Money and Participants at WC"])
    
    if subpage == "Averages throughout the years":
        st.title("Development of Price Money and the Number of Participants of the World Championship")
        fig = plot_winning_averages()
        st.plotly_chart(fig)
        
    elif subpage == "Price Money and Participants at WC":
        st.title("Participants of the World Championships over the Years")
        fig = plot_participants()
        st.plotly_chart(fig)
        
        st.title("Price Money of the World Championships over the Years")
        fig = plot_price_money
        st.plotly_chart(fig)
        
        st.title("Participants and Price Money of the World Championships over the Years")
        fig = plot_price_money_and_participants()
        st.plotly_chart(fig)
        
elif page == "Strategies and Tactics":
    subpage = st.sidebar.radio("Strategies and Tactics", ["Location of Tournament and Winner Nationality", "Team vs. Single", "Double Fields"])
    
    if subpage == "Location of Tournament and Winner Nationality":
        st.title("Observed Frequencies")
        fig = plot_observed_frequencies
        st.plotly_chart(fig)
        
        st.title("Difference between Observed and Expected Frequencies")
        fig = plot_observed_expected_frequencies
        st.plotly_chart(fig)
        
        st.title("Conditional Probabilities")
        fig = plot_conditional_probability
        st.plotly_chart(fig)
        
    elif subpage == "Team vs. Single":
        st.title("Comparision of Averages of the Team Matches to the Averages of the Single Player")
        fig = plot_comparison_single_team
        st.plotly_chart(fig)
        
    elif subpage == "Double Fields":
        st.title("Hit and Misses of individual Double Fields")
        fig = plot_doubles_fields_hits_misses()
        st.plotly_chart(fig)
        
        st.title("Disctribution of Throws and Hits on Double Fields")
        fig = plot_distribution_double_fields()
        st.plotly_chart(fig)
        
        st.title("Doubles Field Values of a specific Player")
        fig = plot_double_fields_player()
        st.plotly_chart(fig)
        
        st.title("Throws on a specific Double Field and its Double Quota of a specific Player")
        fig = plot_double_fields_player_combined()
        st.plotly_chart(fig)
        
elif page == "Players":
    subpage = st.sidebar.radio("Players", ["Averages of Best Players", "Rankings vs Properties"])
    
    if subpage == "Averages of Best Players":
        st.title("Development of Averages in 2009 vs. 2024")
        fig = plot_average_2009_2024()
        st.plotly_chart(fig)
        
        st.title("Development of Averages over the Years")
        fig = plot_average_every_year()
        st.plotly_chart(fig)
        
        st.title("Development of Checkouts in 2012 vs. 2024")
        fig = plot_checkout_2012_2024()
        st.plotly_chart(fig)
        
        st.title("Development of Checkouts over the Years")
        fig = plot_checkout_every_year()
        st.plotly_chart(fig)
        
    elif subpage == "Rankings vs Properties":
        st.title("Participants Over the Years")
        #fig = question_6()
        #st.plotly_chart(fig)
        
    