darts_explanation = """Darts is a competitive sport in which two players take alternating turns throwing three darts at a dartboard. The game is highly analytical, as tournaments and rankings rely heavily on scores, averages, and overall statistics. Numerous websites and analysts track the sport by gathering extensive numerical data, monitoring the throws across multiple matches, and covering the latest news and developments within the darts community.

The dartboard is split up like a pizza of 20 slices, wherein these slices have two large fields (single fields) along with smaller double and triple fields that multiply the respective number's value. At the center of the board, there are two circular target areas: the outer bull, worth 25 points, and the inner bullseye, worth 50 points. The bullseye functions as the board's double for the bull. The triple 20, with it's 60 points, is the highest score on the board. This means the highest score to be reached with three darts is 180.

Matches are structured in different ways depending on the event. The leg-format we focused on lets players compete to win a predetermined number of legs e.g. best of 11 legs, meaning the first to six wins. Within a leg, the players start with a score of 501 and aim to reduce it to exactly zero, finishing with a double. The hightest value to do a checkout with (finish a leg) is 170. This concept makes players have to calculate their next throwing options to check out efficiently. The bullseye with its 50 points is the highest double field for a checkout, which doesn't mean that it is targeted the most to finish a leg. A player's checkout quota is another crucial statistic in darts, representing the percentage of times a player successfully finishes a leg when given the opportunity. A high checkout percentage indicates a player's efficiency in closing out legs under pressure.

Over the course of a match, the average points a player throws with one dart is calculated. Averages are one of the most critical statistics in darts. The primary metric used is the three-dart average, which is calculated by dividing a player's total points scored in a throw divided by 3 (number of dart in a throw). This gives an indication of a player's overall scoring efficiency and consistency. A high three-dart average is a strong indicator of skill, as it reflects a player's ability to hit high-scoring targets consistently while maintaining accuracy. Professional players often maintain averages above 90, with the elite players frequently surpassing 100.

Darts players earn rankings throughout various tournaments, accumulating points based on results. The most known rankings is the PDC Order of Merit. In this, a player's rank is determined by prize money earned over the last two years in ranking events."""


data_pipeline = """This data science project focuses on darts and aims to transform raw data into structured datasets suitable for visualization and analysis. The goal is to answer predefined research questions by gathering data from multiple sources, processing it, and generating analytical datasets.

The project began with formulating research questions, ensuring they were answerable with the available data (looking ahead at available data sources), and prioritizing those that were the most interesting and meaningful. After defining these questions, relevant data sources were identified. Since existing APIs did not provide sufficient information, web scraping was necessary. The data was acquired from several sources, including:

- Darts Orakel:
https://app.dartsorakel.com/

- Mastercaller PDC World Championship:
https://mastercaller.com/tournaments/pdc-world-championship/

- Dartn.de Professional Darts:
https://www.dartn.de/Dart-Profis

- Wikipedia - Professional Darts Corporation:
https://de.wikipedia.org/wiki/Professional_Darts_Corporation

- Wikipedia - PDC World Darts Championship:
https://de.wikipedia.org/wiki/PDC_World_Darts_Championship

- Flashscore:
https://www.flashscore.de/


These sources provided a comprehensive range of information, from historical match results and official player statistics to tournament formats and prize money distributions.

The data pipeline followed a structured process, including acquisition, processing, transformation, visualization, and analysis.

The first stage, data acquisition, involved extracting player statistics, match results, and other relevant information through those multiple web scraping programs. The data was manually validated to ensure completeness and correctness before storing it in structured CSV files.

The custom scraping scripts were developed for each research question, extracting structured data from website HTML using Selenium and BeautifulSoup. Browser automation was set up using the Chrome WebDriver and automated WebDriver management with ChromeDriverManager. Data extraction followed a systematic process, filtering relevant information and organizing it into pandas DataFrames. These DataFrames were structured consistently and combined into comprehensive datasets. Each dataset was then exported into separate CSV files, categorized by research question and additional information, such as rankings and additional player statistics.

Once the raw data was extracted, the transformation phase began. CSV datasets were manually cleaned, filtered, and prepared for visualization. Any missing values affecting the research questions were addressed, and errors in the corresponding web scraping programs were corrected when necessary. Data visualization was an essential part of the project, as the research questions were not meant to be answered solely through graphs but together with explanatory text snippets on the website and poster. Together they are meant to provide meaningful insights into the game and its statistics.

The execution flow of the pipeline started with defining the research questions and identifying data sources. Web scraping scripts were then developed and executed to extract structured data. The extracted data was validated, cleaned, and stored in organized CSV files. In the next step, datasets were transformed to ensure correctness and consistency, addressing any missing values or errors manually. The final datasets were then analyzed and visualized using appropriate graphical representations, forming the basis for answering the research questions. The results were interpreted and integrated into the website and poster to present meaningful insights in an interactive way."""