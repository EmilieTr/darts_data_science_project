darts_explanation = """Darts is a competitive sport in which two players take alternating turns throwing three darts at a dartboard.
The game is highly analytical, as tournaments and rankings rely heavily on scores, averages, and overall statistics. Numerous websites
and analysts track the sport by gathering extensive numerical data, monitoring the throws across multiple matches,
and covering the latest news and developments within the darts community.

The dartboard is split up like a pizza of 20 slices, wherein these slices have two large fields (single fields) along with smaller double and
triple fields that multiply the respective number's value. At the center of the board, there are two circular target areas: the outer bull, worth 25 points,
and the inner bullseye, worth 50 points. The bullseye functions as the board's double for the bull. The triple 20, with it's 60 points,
is the highest score on the board. This means the highest score to be reached with three darts is 180.

Matches are structured in different ways depending on the event. The leg-format we focused on lets players compete to win a predetermined
number of legs e.g. best of 11 legs, meaning the first to six wins. Within a leg, the players start with a score of 501 and aim to reduce it to exactly zero,
finishing with a double. The hightest value to do a checkout with (finish a leg) is 170. This concept makes players have to calculate their
next throwing options to check out efficiently. The bullseye with its 50 points is the highest double field for a checkout, which doesn't mean that it is
targeted the most to finish a leg. A player's checkout quota is another crucial statistic in darts, representing the percentage of times a player
successfully finishes a leg when given the opportunity. A high checkout percentage indicates a player's efficiency in closing out legs under pressure.

Over the course of a match, the average points a player throws with one dart is calculated. Averages are one of the most critical statistics in darts.
The primary metric used is the three-dart average, which is calculated by dividing a player's total points scored in a throw
divided by 3 (number of dart in a throw). This gives an indication of a player's overall scoring efficiency and consistency. A high three-dart average is a
strong indicator of skill, as it reflects a player's ability to hit high-scoring targets consistently while maintaining accuracy. Professional players
often maintain averages above 90, with the elite players frequently surpassing 100.

Darts players earn rankings throughout various tournaments, accumulating points based on results. The most known rankings is the PDC Order of Merit.
In this, a player's rank is determined by prize money earned over the last two years in ranking events."""


data_pipeline = """This data science project focuses on darts and aims to transform raw data into structured datasets suitable for visualization and analysis.
The goal is to answer predefined research questions by gathering data from multiple sources, processing it, and generating analytical datasets.

The project began with formulating research questions, ensuring they were answerable with the available data (looking ahead at available data sources),
and prioritizing those that were the most interesting and meaningful. After defining these questions, relevant data sources were identified.
Since existing APIs did not provide sufficient information, web scraping was necessary. The data was acquired from several sources, including:

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


These sources provided a comprehensive range of information, from historical match results and official player statistics to tournament formats and
prize money distributions.

The data pipeline followed a structured process, including acquisition, processing, transformation, visualization, and analysis.

The first stage, data acquisition, involved extracting player statistics, match results, and other relevant information through those multiple
web scraping programs. The data was manually validated to ensure completeness and correctness before storing it in structured CSV files.

The custom scraping scripts were developed for each research question, extracting structured data from website HTML using Selenium and BeautifulSoup.
Browser automation was set up using the Chrome WebDriver and automated WebDriver management with ChromeDriverManager. Data extraction followed
a systematic process, filtering relevant information and organizing it into pandas DataFrames. These DataFrames were structured consistently and
combined into comprehensive datasets. Each dataset was then exported into separate CSV files, categorized by research question and additional information,
such as rankings and additional player statistics.

Once the raw data was extracted, the transformation phase began. CSV datasets were manually cleaned, filtered, and prepared for visualization.
Any missing values affecting the research questions were addressed, and errors in the corresponding web scraping programs were corrected when necessary.
Data visualization was an essential part of the project, as the research questions were not meant to be answered solely through graphs but together with
explanatory text snippets on the website and poster. Together they are meant to provide meaningful insights into the game and its statistics.

The execution flow of the pipeline started with defining the research questions and identifying data sources. Web scraping scripts were then developed and
executed to extract structured data. The extracted data was validated, cleaned, and stored in organized CSV files. In the next step, datasets were
transformed to ensure correctness and consistency, addressing any missing values or errors manually. The final datasets were then analyzed and visualized
using appropriate graphical representations, forming the basis for answering the research questions. The results were interpreted and integrated into the
website and poster to present meaningful insights in an interactive way."""

first_graph_1 = """The line graph comparing 2009 vs. 2024 shows a significant improvement in player averages across all ranking positions.
The 2024 line (blue) consistently remains higher than the 2009 line (purple), indicating that players at all ranking levels are performing
at higher averages than their counterparts from 15 years ago."""

second_graph_1 = """This bar chart shows the progression of averages from 2009 to 2024, with some interesting patterns:

- Starting at 92.0 in 2009, averages initially dipped to 90.0 in 2010

- Consistent improvement through 2012-2013 (97.0)

- A peak of 99.0 in 2017

- Relatively stable high performance (97.0-98.0) from 2019 through 2024"""

third_graph_1 = """In the check-out analytics we have found:

- In 2012, there was more variability in checkout percentages based on rank
- By 2024, checkout percentages have become more consistent across ranks (around 41%)
- Top players (rank 1) had higher checkout percentages in 2012 than in 2024
- Lower-ranked players (ranks 4-5) have improved their checkout percentages compared to 2012"""

interpretation_1 = """In general we can say that the average performance metrics have increased significantly from 2009 to 2024, with approximately
a 7-10 point improvement in averages across all ranking positions.

The data also suggests that the gap between top-ranked and lower-ranked players has decreased over time.

The sport has become more consistent in general as seen in significant improvements between 2009-2017 and seemingly performance metrics stabilized in
recent years (2019-2024), suggesting the sport may have reached a certain maturity level.

The checkout percentages have also become more uniform across different ranking positions, indicating more consistent finishing skills throughout the
professional ranks."""

first_graph_2 = """While the World Championship average scores appear more volatile with sharper peaks and valleys, they seem higher than in the other majors.

Both lines show an upward trajectory from 2000 to 2025 and the average scores generally range between 94 and 105, with a few notable exceptions.

These entail a significant spike around 2015-2016 for World Championship scores, reaching above 105 and a noticeable dip in both averages around 2002-2003.

All these factors seem to rise more, since World Championship scores appear to be trending upward and the gap between World Championship and all major
tournaments has widened slightly in recent years (2022-2025).

This likely comes from improving player skill levels, technological advancements in equipment, and possibly changes in competitive formats or scoring
systems over time."""

first_graph_4 = """Most Attempted Double Fields (Throws):

1. D20 - 14.8%
2. D16 - 11.3%
3. D10 - 11.0%
4. D8 - 10.3%
5. D18 - 7.22%

Most Successfully Hit Double Fields (Hits):

1. D20 - 24.7%
2. D10 - 19.0%
3. D16 - 12.7%
4. D8 - 9.38%
5. D12 - 5.92%

This shows that D20, D16, D10, and D8 are consistently among the most popular double fields for both attempts and successful hits."""

second_graph_4 = """The best players achieve checkout success rates of 50-67% on their preferred doubles.

The preferred double felds vs. succesful double hits indicate that top players focus on just two double fields (D20 and D16), because ..."""

first_graph_5 = """This participant growth pattern reveals deliberate structural changes to the tournament format, with significant expansions
occurring around 1999, 2006, and 2019.

The total prize pool has seen remarkable growth:

- Started at £64,000 in 1994
- Reached £1 million by 2010
- Peaked at £2.5 million in 2019 and has remained stable since

The winner's prize has followed a similar trajectory:

- £16,000 in 1994
- £100,000 by 2006
- £250,000 by 2014
- £500,000 from 2019 onward

There's a clear correlation between participant numbers and prize money:

- Major increases in participants (1999, 2006, 2019) typically coincided with significant prize money increases
- The 2019 expansion to 96 participants aligned with the prize pool reaching its current £2.5 million
- Since 2019, both participant numbers and prize money have remained stable

The graphs show that while the total prize pool has increased, the distribution maintains a similar structure:

- Champion and runner-up consistently receive the largest portions
- Prize money decreases progressively across placement categories
- The introduction of new placement categories (Last 64 in 2006, Last 96 in 2019) reflects the expanding tournament format"""

first_graph_6 = """The peak performance age for players seems to be 30-50 years, with some older players (50-60) still ranking well."""

second_graph_6 = """England appears most frequently, indicating that English players may dominate the rankings.

The majority of top-ranking players come from England, suggesting that the sport might be more competitive or better developed there.
Other countries like Germany, Japan, and Australia have representation, but their players are less frequent.
Players from these countries might just be less common."""

third_graph_6 = """The majority of high-ranking players are right-handed, as shown by the larger bubbles on the left.
Left-handed players are significantly fewer and rarely appear in top ranks.

Right-handed players dominate the rankings, suggesting that left-handed players are either less common or struggle to keep up."""

first_graph__7 = """While English players have won the most tournaments overall (130 wins), followed by Dutch players (70 wins), this reflects the
general dominance of these nations in darts rather than a host country advantage."""

second_graph_7 = """This graph displays the residuals from a statistical analysis, likely a chi-square test. The values are relatively small, indicating minimal
deviation from what would be expected if there were no relationship between host country and winner nationality."""

third_graph_7 = """Conditional Probabilities show the probability of winners being from a specific nationality given the host country. The conditional probabilities
appear fairly consistent across host countries:

- In Australia, England, and USA, English players win about 43-44% of tournaments
- In the Netherlands, Dutch players win 29% of tournaments
- No pattern suggests players consistently perform better in their home countries"""

fourth_graph_7 = """The UK and Germany host the most tournaments."""

first_graph_8 = """Something could be written here."""

second_graph_8 = """Game Insider for Analysis: team matches only occurr at the World Cup.

Most countries show a positive difference in the purple bars, indicating that players generally perform better individually than when playing as part of a team.

Highlights:

(Notable standouts:

ENG (England) shows the highest positive difference, with approximately 525+ players performing better individually than in team matches over the years analyzed.
WAL (Wales), NED (Netherlands), and SCO (Scotland) also show substantial positive differences.


Negative differences: Some countries show significant negative differences (orange bars), meaning players performed worse individually than in team settings:

NED (Netherlands) has the most dramatic negative difference, with approximately 350 players performing worse individually.
Other countries with notable negative differences include BRA (Brazil), HUN (Hungary), and SWE (Sweden).)
Does this have to do with the UK being better represented and us only showcasing absolute values or maybe is it that people try harder in World Cups?"""

first_graph_15 = """individual analysis for players???"""
