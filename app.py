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
        <a href="mailto:stu240535@mail.uni-kiel.de">Emilie Terhaars Stu-Mail</a> |
        <a href="mailto:stu240535@mail.uni-kiel.de">Sara Rolfs Stu-Mail</a> |
        <a href="www.google.com">poster link here?</a>
    </div>
    """
    st.markdown(footer_code, unsafe_allow_html=True)


# Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Tournament Data", "Player Data", "Data Pipeline"])

# Change page
if page == "Home":
    st.title("Welcome to this Data Science Project!")
    st.header("Here you can find interesting Research Questions on the Game Darts")
    st.subheader("This is a Dashboard")
    with st.expander("Game Explanation"):
        st.write(darts_explanation)
    st.write("Testtest")    

    # Call function to add footer
    add_footer()

elif page == "Tournament Data":
    subpage = st.sidebar.radio(
        "Tournament Data",
        [
            "2 Averages over Time",
            "5 Price Money and Participants at WC",
            "7 Locations of Tournaments and Winner Nationality"
        ]
    )

    # Question 2
    if subpage == "2 Averages over Time":
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
            "of the World Championship (gehört das nicht in 5)"
        )
        
        # Call the function with the list of selected tournaments
        fig = plot_winning_averages(selected_tournaments)
        st.plotly_chart(fig)

        st.write(first_graph_2)

        # Call function to add footer
        add_footer()
        
    # Question 5
    elif subpage == "5 Price Money and Participants at WC":
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

        st.write(first_graph_5)

        # Call function to add footer
        add_footer()
        
    # Question 7
    if subpage == "7 Locations of Tournaments and Winner Nationality":
        st.header(
            "7. How does the country a tournament is held in correlate "
            "to the success of players?"
        )
        
        st.subheader("Observed Frequencies")
        fig = plot_observed_frequencies()
        st.plotly_chart(fig)

        st.write(first_graph__7)
        
        st.subheader("Difference between Observed and Expected Frequencies")
        fig = plot_observed_expected_frequencies()
        st.plotly_chart(fig)

        st.write(second_graph_7)
        
        st.subheader("Conditional Probabilities")
        fig = plot_conditional_probability()
        st.plotly_chart(fig)

        st.write(third_graph_7)
        
        st.image("Visualizations/question_7/map.png")

        st.write(fourth_graph_7)

        # Call function to add footer
        add_footer()

elif page == "Player Data":
    subpage = st.sidebar.radio(
        "Player Data", 
        [
            "1 Averages of the Best Players",
            "6 Rankings vs. Properties",
            "8 Team vs. Single",
            "4 Popular Double Fields",
            "15 Player Stats",
            "9 Likelihood of 180 after 180",
            "10 Winning Legs after starting with 180"
        ]
    )
    
    # Question 8
    if subpage == "8 Team vs. Single":
        st.header("8. How much do a player's team and single performance "
                 "differ?")
        
        st.subheader("Comparision of Checkouts of the Team Matches to the Averages of the Single Player")
        fig = plot_comparison_single_team_checkout()
        st.plotly_chart(fig)
        
        st.write(first_graph_8)

        st.subheader(
            "Comparision of Averages of the Team Matches to the Averages "
            "of the Single Player"
        )
        fig = plot_comparison_single_team_averages()
        st.plotly_chart(fig)

        st.write(second_graph_8)

        # Call function to add footer
        add_footer()

    # Question 15
    elif subpage == "15 Player Stats":
        st.header(
            "15. How does the performance of individual players change over "
            "time?"
        )
        
        st.write(first_graph_15)
        
        # Load a list of players from CSV or define manually
        players = [
            "Luke Humphries", "Luke Littler", "Michael van Gerwen",
            "Phil Taylor", "Stephen Bunting", "Rob Cross", "Gerwyn Price",
            "Nathan Aspinall", "Chris Dobey", "Gary Anderson", "James Wade",
            "Peter Wright", "Martin Schindler"
        ]  # Replace with real names or load from a file
        
        # Dropdowns for selecting player and double field
        selected_player = st.selectbox("Select a Player", players)
        
        # Retrieve player data
        csv_file = "Data/question 6/male_players.csv"
        df = pd.read_csv(csv_file)
        player_data = df[df["Name"] == selected_player].iloc[0]

        # Display player profile
        st.header(player_data["Name"])
        st.write(f"**Nationality:** {player_data['Nationality']}")
        st.write(f"**Date of Birth:** {player_data['Geburtstag']}")
        st.write(f"**Playing since:** {player_data['Plays since']}")
        st.write(f"**Professional since:** {player_data['Profi since']}")
        st.write(f"**Handedness:** {player_data['Handedness']}")
        st.write(f"**Darts Used:** {player_data['Darts gramm']}")
        
        st.subheader(f"Double Field Values of {selected_player}")
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
    elif subpage == "4 Popular Double Fields":
        st.header(
            "4. What are most popular double fields and their "
            "corresponding checkout quotes?"
        )
        
        st.subheader("Distribution of Throws and Hits on Double Fields")
        fig = plot_distribution_double_fields()
        st.plotly_chart(fig)

        st.write(first_graph_4)
        
        st.subheader(
            "Distribution of Throws and Hits on the Best Double Fields "
            "per Player"
        )
        fig = plot_distribution_best_double_fields()
        st.plotly_chart(fig)

        st.write(second_graph_4)
    
        # Call function to add footer
        add_footer()

    # Question 1
    elif subpage == "1 Averages of the Best Players":
        st.header("1. How does the general performance of players change over "
                 "time?")
        
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

            st.write(first_graph_1)
            
            st.subheader("Development of Averages over the Years")
            fig = plot_average_every_year(selected_ranking_position)
            st.plotly_chart(fig)

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

            st.write(third_graph_1)
        
        st.write(interpretation_1)        
    
        # Call visualizations with selected features
        # st.title("Hit and Misses of individual Double Fields")
        # fig = plot_doubles_fields_hits_misses()
        # st.plotly_chart(fig)  
        
        # Call function to add footer
        add_footer()

    # Question 6
    elif subpage == "6 Rankings vs. Properties":
        st.header("6. How does age, nationality and handiness effects "
                 "the rankings?")
        
        # Erstelle einen Slider von 0 bis 50
        var = st.slider("Choose a Number", min_value=1, max_value=50)
        variant = st.radio("Choose an Option", ("absolute values", "relative values"))
        
        if variant == "absolute values":
            variant = 1
        else:
            variant = 0
        
        st.subheader("Age Participants Over the Years")
        fig, _ = plot_ranking_age(var, variant)
        st.plotly_chart(fig)

        st.write(first_graph_6)
        
        st.subheader("Nationality Participants Over the Years")
        fig, _ = plot_ranking_nationality(var, variant)
        st.plotly_chart(fig)

        st.write(second_graph_6)
        
        st.subheader("Handedness Participants Over the Years")
        fig, _ = plot_ranking_handedness(var, variant)
        st.plotly_chart(fig)

        st.write(third_graph_6)

        # Call function to add footer
        add_footer()
        
    # Question 9    
    elif subpage == "9 Likelihood of 180 after 180":
        st.header("9. How likely is it to throw a 180 after the opponent threw one?")
        
        df = pd.read_csv('Visualizations/question_9/180_stats.csv')
        st.dataframe(df)

        st.write(first_graph_9)
        
    # Question 10     
    elif subpage == "10 Winning Legs after starting with 180":  
        st.header("10. How likely are participants win a leg after throwing a 180 as first throw?") 
        
        df = pd.read_csv('Visualizations/question_10/180_stats.csv') 
        st.dataframe(df)

        st.write(first_graph_10)

elif page == "Data":
    st.title("Data Pipeline")
    st.header("Our Process of data aquisition, data transformation, and data visualization.")
    st.write(data_pipeline)

    # Call function to add footer
    add_footer()