import streamlit as st
import pandas as pd
from Visualizations.question_1 import (
    plot_checkout_every_year,
    plot_checkout_line_chart,
    plot_average_every_year,
    plot_average_line_chart
)
from Visualizations.question_2 import plot_winning_averages
from Visualizations.question_15 import (
    plot_double_fields_player_combined,
    plot_double_fields_player,
    plot_player_average
)
from Visualizations.question_4 import (
    plot_distribution_double_fields,
    plot_distribution_best_double_fields
)
from Visualizations.question_5 import (
    plot_prize_money_and_participants,
    plot_participants,
    plot_prize_money
)
from Visualizations.question_6 import (
    plot_ranking_age,
    plot_ranking_nationality,
    plot_ranking_handedness
)
from Visualizations.question_7 import (
    plot_observed_frequencies,
    plot_observed_expected_frequencies,
    plot_conditional_probability
)
from Visualizations.question_8 import (
    plot_comparison_single_team_checkout,
    plot_comparison_single_team_averages
)
from texts import *
# from Visualizations.question_9 import


def add_footer():
    footer_code = """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #F0F2F6;
            color: black;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
        a {
            color: #fff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
    <div class="footer">
        Contact: <a href="mailto:stu240535@mail.uni-kiel.de">stu240535@mail.uni-kiel.de</a> |
        <a href=www.google.com">this is a link</a>
    </div>
    """
    st.markdown(footer_code, unsafe_allow_html=True)


# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Tournaments", "Players", "Data"])

# Change page
if page == "Home":
    st.title("Welcome to this Data Science Project!")
    st.header("Here you can find interesting Research Questions on the Game Darts")
    st.subheader("This is a Dashboard")
    with st.expander("Game Explanation"):
        st.write(darts_explanation)
    st.write("Testtext")

    # Call function to add footer
    add_footer()

elif page == "Tournaments":
    subpage = st.sidebar.radio(
        "Development of Tournaments",
        [
            "2 Averages throughout the years",
            "5 Price Money and Participants at WC",
            "7 Location of Tournament and Winner Nationality"
        ]
    )

    # Question 2
    if subpage == "2 Averages throughout the years":
        tournaments = [
            "World Championship",
            "World Matchplay",
            "World Grand Prix",
            "Grand Slam",
            "Players Championship Finals",
            "World Cup",
            "World Series of Darts Finals",
            "European Tour",
            "Players Championship",
            "World Series"
        ]
        
        st.header("2. How do the averages of tournaments vary over time?")
        
        # Select multiple tournaments
        selected_tournaments = st.multiselect(
            "Select Tournaments",
            tournaments,
            default=["World Championship"]
        )
        
        # Display the selected tournament
        st.subheader(
            "Development of Prize Money and the Number of Participants "
            "of the World Championship"
        )
        
        # Call the function with the list of selected tournaments
        fig = plot_winning_averages(selected_tournaments)
        st.plotly_chart(fig)

        # Call function to add footer
        add_footer()
        
    # Question 5
    elif subpage == "5 Price Money and Participants at WC":
        st.header("5. How does the price money and number of participants vary "
                 "over time?")
        
        st.subheader("Participants of the World Championships over the Years")
        fig = plot_participants()
        st.plotly_chart(fig)
        
        st.subheader("Price Money of the World Championships over the Years")
        fig = plot_prize_money()
        st.plotly_chart(fig)
        
        st.subheader(
            "Participants and Price Money of the World Championships "
            "over the Years"
        )
        fig = plot_prize_money_and_participants()
        st.plotly_chart(fig)

        # Call function to add footer
        add_footer()
        
    # Question 7
    if subpage == "7 Location of Tournament and Winner Nationality":
        st.header(
            "7. How does the country a tournament is held in correlate "
            "to the success of players?"
        )
        
        st.subheader("Observed Frequencies")
        fig = plot_observed_frequencies()
        st.plotly_chart(fig)
        
        st.subheader("Difference between Observed and Expected Frequencies")
        fig = plot_observed_expected_frequencies()
        st.plotly_chart(fig)
        
        st.subheader("Conditional Probabilities")
        fig = plot_conditional_probability()
        st.plotly_chart(fig)
        
        st.image("Visualizations/question_7/map.png")

        # Call function to add footer
        add_footer()

elif page == "Players":
    subpage = st.sidebar.radio(
        "Players", 
        [
            "1 Averages of Best Players",
            "6 Rankings vs Properties",
            "8 Team vs. Single",
            "4 Double Fields",
            "15 Player Stats"
        ]
    )
    
    # Question 8
    if subpage == "8 Team vs. Single":
        st.header("8. How much do a player's team and single performance"
                 "differ?")
        
        st.subheader("Comparision of Checkouts of the Team Matches to the Averages of the Single Player")
        fig = plot_comparison_single_team_checkout()
        st.plotly_chart(fig)
        
        st.subheader(
            "Comparision of Averages of the Team Matches to the Averages "
            "of the Single Player"
        )
        fig = plot_comparison_single_team_averages()
        st.plotly_chart(fig)

        # Call function to add footer
        add_footer()

    # Question 15
    elif subpage == "15 Player Stats":
        st.header(
            "15. How does the performance of individual players change over "
            "time?"
        )
        
        # Load a list of players from CSV or define manually
        players = [
            "Luke Humphries", "Luke Littler", "Michael van Gerwen",
            "Phil Taylor", "Stephen Bunting", "Rob Cross", "Gerwyn Price",
            "Nathan Aspinall", "Chris Dobey", "Gary Anderson", "James Wade",
            "Peter Wright", "Martin Schindler"
        ]  # Replace with real names or load from a file
        
        # Dropdowns for selecting player and double field
        selected_player = st.selectbox("Select a Player", players)
        
        st.subheader(f"Doubles Field Values of {selected_player}")
        fig = plot_double_fields_player(selected_player)
        st.plotly_chart(fig)
        
        double_fields = [f"D{i}" for i in range(1, 21)] + ["D25"]  # Double fields
        selected_double = st.selectbox("Select a Double Field", double_fields)
        
        st.subheader(
            f"Throws on {selected_double} and its Double Quota "
            f"for {selected_player}"
        )
        fig = plot_double_fields_player_combined(selected_player, selected_double)
        st.plotly_chart(fig)
        
        st.subheader(
            f"Averages for {selected_player}"
        )
        fig = plot_player_average(selected_player)
        st.plotly_chart(fig)

        # Call function to add footer
        add_footer()
    
    # Question 4
    elif subpage == "4 Double Fields":
        st.header(
            "4. What are most popular double fields and what are "
            "the corresponding checkout quotes?"
        )
        
        st.subheader("Distribution of Throws and Hits on Double Fields")
        fig = plot_distribution_double_fields()
        st.plotly_chart(fig)
        
        st.subheader(
            "Distribution of Throws and Hits on the Best Double Fields "
            "per Player"
        )
        fig = plot_distribution_best_double_fields()
        st.plotly_chart(fig)
    
        # Call function to add footer
        add_footer()

    # Question 1
    elif subpage == "1 Averages of Best Players":
        st.header("1. How does the performance of players in general "
                 "change over time?")
        
        category = ["Averages", "Checkout Quota"]
        ranking_positions = [5, 10, 15, 20]
        selected_category = st.selectbox("Select a Category", category)
        selected_ranking_position = st.selectbox(
            "Select a Number of Ranking Positions",
            ranking_positions
        )
        
               
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
            
            st.subheader("Development of Averages over the Years")
            fig = plot_average_every_year(selected_ranking_position)
            st.plotly_chart(fig)
            
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
    
        # Call visualizations with selected features
        # st.title("Hit and Misses of individual Double Fields")
        # fig = plot_doubles_fields_hits_misses()
        # st.plotly_chart(fig)  
        
        # Call function to add footer
        add_footer()

    # Question 6
    elif subpage == "6 Rankings vs Properties":
        st.header("6. How does age, nationality and handiness effects "
                 "the rankings?")
        
        var = 10
        
        st.subheader("Age Participants Over the Years")
        fig = plot_ranking_age(var)
        st.plotly_chart(fig)
        
        st.subheader("Nationality Participants Over the Years")
        fig = plot_ranking_nationality(var)
        st.plotly_chart(fig)
        
        st.subheader("Handedness Participants Over the Years")
        fig = plot_ranking_handedness(var)
        st.plotly_chart(fig)

        # Call function to add footer
        add_footer()

elif page == "Data":
    st.title("Data Pipeline")
    st.header("Our Process of data aquisition, data transformation, and data visualization.")
    st.write(data_pipeline)

    # Call function to add footer
    add_footer()