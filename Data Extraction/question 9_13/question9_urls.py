from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# List of URLs for major darts tournaments on Flashscore
majors = [
    "https://www.flashscore.de/dart/welt/world-matchplay/ergebnisse/",
    "https://www.flashscore.de/dart/welt/world-grand-prix/ergebnisse/",
    "https://www.flashscore.de/dart/welt/players-championship-finals/ergebnisse/",
    "https://www.flashscore.de/dart/welt/grand-slam/ergebnisse/",
    "https://www.flashscore.de/dart/welt/pdc-world-masters/ergebnisse/",
    "https://www.flashscore.de/dart/welt/world-series-finals/ergebnisse/",
    "https://www.flashscore.de/dart/vereinigtes-konigreich/uk-open/ergebnisse/",
    "https://www.flashscore.de/dart/welt/premier-league/ergebnisse/"
]

# List of URLs for European Tour events (1 to 13)
european_tour = []
for number in range(1, 14):
    european_tour.append(
        "https://www.flashscore.de/dart/europa/european-tour-" 
        + str(number) 
        + "/ergebnisse/"
    )

# Combine major and European Tour tournament URLs
urls = majors + european_tour

# Dictionary to store tournament names and their respective match links
tournament_links = {}

# Automatically download and use the correct WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

for url in urls:
    
    # Open the tournament page
    driver.get(url)

    # Wait for the page to fully load
    time.sleep(2)

    # Get the page source
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find all links that end with 'spiel-zusammenfassung' (match summary)
    links = [
        a['href'] for a in soup.find_all(
            'a', 
            href=lambda href: href and href.endswith('spiel-zusammenfassung')
        )
    ]
    
    # Extract the tournament name from the URL
    tournament = url.split('/')[-3].replace('-', ' ')
    
    # Store the links in the dictionary under the tournament name
    tournament_links[tournament] = links
    print(len(links))
    
print(tournament_links)

# Close the WebDriver
driver.quit()   

# Write the extracted links to a text file
with open('./Data Extraction/urls_flashcore.txt',
           'w', encoding="iso 8859-1") as file:
    for key, value in tournament_links.items():
        file.write(f'{key}: {value}\n')
