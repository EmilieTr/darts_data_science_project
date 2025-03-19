# :earth_americas: GDP dashboard template

A simple Streamlit app showing the GDP of different countries in the world.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gdp-dashboard-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```


Local URL: http://localhost:8501
Network URL: http://10.0.4.173:8501
External URL: http://172.191.151.56:8501

# :dart: Data Science Project
(bla bli blubb)

### Research Questions
Tournaments:
- „How do the averages of tournaments vary over time?"
- „How does the price money and number of participants vary over time?“
- „How does the country a tournament is held in correlate to the success of players?“

Players:
- „How does the performance of players in general change over time?“
-    „How does the performance of players change over time?“
-    "What are the are most popular double fields and what are the generally corresponding checkout quotes?“

- „How does the performance of individual players change over time?
-    „What are most popular double fields and what are the corresponding checkout quotes?“
- „How does age, nationality and handiness effects the rankings?“
- „Is there a difference between a player's team performance and single performance?“

### Data

## Interesting Darts Questions answered with a few clicks
(website demo)

### Features
- Explanation of the game
- Toggle into different subtopics
- Interactive Graphs
- Data Analysis at first glance
- 

## Development

### Data Pipeline

This data science project focuses on darts and aims to transform raw data into structured datasets suitable for visualization and analysis. The goal is to answer predefined research questions by gathering data from multiple sources, processing it, and generating analytical datasets.

The project began with formulating research questions, ensuring they were answerable with the available data (looking ahead at available data sources), and prioritizing those that were the most interesting and meaningful. After defining these questions, relevant data sources were identified. Since existing APIs did not provide sufficient information, web scraping was necessary. The data was acquired from several sources, including:

Darts Orakel
- Darts Orakel: https://app.dartsorakel.com/
- Mastercaller PDC World Championship: https://mastercaller.com/tournaments/pdc-world-championship/
- Dartn.de Professional Darts: https://www.dartn.de/Dart-Profis
- Wikipedia - Professional Darts Corporation: https://de.wikipedia.org/wiki/Professional_Darts_Corporation
- Wikipedia - PDC World Darts Championship: https://de.wikipedia.org/wiki/PDC_World_Darts_Championship
- Flashscore: https://www.flashscore.de/
These sources provided a comprehensive range of information, from historical match results and official player statistics to tournament formats and prize money distributions.

The data pipeline followed a structured process, including acquisition, processing, transformation, visualization, and analysis.

The first stage, data acquisition, involved extracting player statistics, match results, and other relevant information through those multiple web scraping programs. The data was manually validated to ensure completeness and correctness before storing it in structured CSV files.

The custom scraping scripts were developed for each research question, extracting structured data from website HTML using Selenium and BeautifulSoup. Browser automation was set up using the Chrome WebDriver and automated WebDriver management with ChromeDriverManager. Data extraction followed a systematic process, filtering relevant information and organizing it into pandas DataFrames. These DataFrames were structured consistently and combined into comprehensive datasets. Each dataset was then exported into separate CSV files, categorized by research question and additional information, such as rankings and additional player statistics.

Once the raw data was extracted, the transformation phase began. CSV datasets were manually cleaned, filtered, and prepared for visualization. Any missing values affecting the research questions were addressed, and errors in the corresponding web scraping programs were corrected when necessary. Data visualization was an essential part of the project, as the research questions were not meant to be answered solely through graphs but together with explanatory text snippets on the website and poster. Together they are meant to provide meaningful insights into the game and its statistics.

The execution flow of the pipeline started with defining the research questions and identifying data sources. Web scraping scripts were then developed and executed to extract structured data. The extracted data was validated, cleaned, and stored in organized CSV files. In the next step, datasets were transformed to ensure correctness and consistency, addressing any missing values or errors manually. The final datasets were then analyzed and visualized using appropriate graphical representations, forming the basis for answering the research questions. The results were interpreted and integrated into the website and poster to present meaningful insights in an interactive way.

- How is the data connected?
- Known issues
- Build with Streamlit
- Avalability (see streamlit plan, only available for people in the CAU-VPN?)
- 
