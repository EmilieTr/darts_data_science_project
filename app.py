import streamlit as st
import pandas as pd
from Visualizations.question_1 import plot_checkout_every_year, plot_average_2009_2024, plot_average_every_year, plot_checkout_2012_2024
from Visualizations.question_2 import plot_winning_averages
from Visualizations.question_4 import plot_double_fields_player_combined, plot_distribution_double_fields, plot_double_fields_player, plot_doubles_fields_hits_misses
from Visualizations.question_5 import plot_price_money_and_participants, plot_participants, plot_price_money
from Visualizations.question_6 import plot_ranking_age
from Visualizations.question_7 import plot_observed_frequencies, plot_observed_expected_frequencies, plot_conditional_probability
from Visualizations.question_8 import plot_comparison_single_team
#from Visualizations.question_9 import 

# Sidebar für Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Development of Tournaments", "Strategies and Tactics", "Players"])

# Seite wechseln  
if page == "Development of Tournaments":
    subpage = st.sidebar.radio("Development of Tournaments", ["Averages throughout the years", "Price Money and Participants at WC"])
    
    # Question 2
    if subpage == "Averages throughout the years":
        tournaments = [
            "All",
            "World Championship",
            "World Matchplay",
            "World Grand Prix",
            "Masters of Darts",
            "PDC US Open", 
            "Grand Slam",
            "Players Championship Finals",
            "World Cup",
            "World Masters",
            "World Series of Darts Finals",
            "Champions League",
            "European Tour", 
            "Players Championship", 
            "World Series"
        ]
        selected_tournament = st.selectbox("Select a Tournament", tournaments)
        
        st.title("2. How do the (average) winning scorings of tournaments/matches vary over the years?")
        
        st.title("Development of Price Money and the Number of Participants of the World Championship")
        fig = plot_winning_averages(selected_tournament)
        st.plotly_chart(fig)
        
    # Question 5
    elif subpage == "Price Money and Participants at WC":
        st.title("5. How does the price money and the amount of participants of tournaments vary over the years?")
        
        st.title("Participants of the World Championships over the Years")
        fig = plot_participants()
        st.plotly_chart(fig)
        
        st.title("Price Money of the World Championships over the Years")
        fig = plot_price_money()
        st.plotly_chart(fig)
        
        st.title("Participants and Price Money of the World Championships over the Years")
        fig = plot_price_money_and_participants()
        st.plotly_chart(fig)
        
elif page == "Strategies and Tactics":
    subpage = st.sidebar.radio("Strategies and Tactics", ["Location of Tournament and Winner Nationality", "Team vs. Single", "Double Fields"])
    
    # Question 7
    if subpage == "Location of Tournament and Winner Nationality":
        st.title("7. In which countries are tournaments held and how does it influence singular participants if at all?")
        
        st.title("Observed Frequencies")
        fig = plot_observed_frequencies()
        st.plotly_chart(fig)
        
        st.title("Difference between Observed and Expected Frequencies")
        fig = plot_observed_expected_frequencies()
        st.plotly_chart(fig)
        
        st.title("Conditional Probabilities")
        fig = plot_conditional_probability()
        st.plotly_chart(fig)
        
    # Question 8
    elif subpage == "Team vs. Single":
        st.title("8. How do team matches compare to single matches in their scores? (does it imply teammates dragging each other down or raising each other up?)")
        
        st.title("Comparision of Averages of the Team Matches to the Averages of the Single Player")
        fig = plot_comparison_single_team()
        st.plotly_chart(fig)
    
    # Question 4   
    elif subpage == "Double Fields":
        st.title("4. What are the most popular double fields and what is the percentage to check them? (doubles are normally not thrown)")
        
        st.title("Double Fields Analysis")

        # Visualisierungen mit gewählten Parametern aufrufen
        #st.title("Hit and Misses of individual Double Fields")
        #fig = plot_doubles_fields_hits_misses()
        #st.plotly_chart(fig)

        st.title("Distribution of Throws and Hits on Double Fields")
        fig = plot_distribution_double_fields()
        st.plotly_chart(fig)        
        
        # Lade eine Liste von Spielern aus einer CSV oder definiere sie manuell
        players = ["Luke Humphries", "Luke Littler", "Michael van Gerwen"]  # Ersetze dies mit echten Namen oder lade aus einer Datei
    
        # Dropdowns für Auswahl des Spielers und Doppelfelds
        selected_player = st.selectbox("Select a Player", players)

        st.title(f"Doubles Field Values of {selected_player}")
        fig = plot_double_fields_player(selected_player)
        st.plotly_chart(fig)
        
        double_fields = [f"D{i}" for i in range(1, 21)] + ["D25"]  # Doppelfelder 1-20, Bullseye D25
        selected_double = st.selectbox("Select a Double Field", double_fields)

        st.title(f"Throws on {selected_double} and its Double Quota for {selected_player}")
        fig = plot_double_fields_player_combined(selected_player, selected_double)
        st.plotly_chart(fig)
        
elif page == "Players":
    subpage = st.sidebar.radio("Players", ["Averages of Best Players", "Rankings vs Properties"])
    
    # Question 1
    if subpage == "Averages of Best Players":
        st.title("1. How do the 5/10/15 best player change from 2000/1995 to now? (averages vs. check-out quota)")
        
        category = ["Averages", "Checkout Quota"] 
        ranking_positions = [5, 10, 15, 20] 
        selected_category = st.selectbox("Select a Category", category)
        selected_ranking_position = st.selectbox("Select a Number of Ranking Positions", ranking_positions)
        
        if selected_category == "Averages":
            st.title("Development of Averages in 2009 vs. 2024")
            fig = plot_average_2009_2024(selected_ranking_position)
            st.plotly_chart(fig)
            
            st.title("Development of Averages over the Years")
            fig = plot_average_every_year()
            st.plotly_chart(fig)
            
        elif selected_category == "Checkout Quota":
            st.title("Development of Checkouts in 2012 vs. 2024")
            fig = plot_checkout_2012_2024(selected_ranking_position)
            st.plotly_chart(fig)
            
            st.title("Development of Checkouts over the Years")
            fig = plot_checkout_every_year()
            st.plotly_chart(fig)
        
    # Question 6
    elif subpage == "Rankings vs Properties":
        st.title("6. How do the rankings vary over age, nationality and left/right handed people of participants?")
        
        var = 10
        
        st.title("Participants Over the Years")
        fig = plot_ranking_age(var)
        st.plotly_chart(fig)