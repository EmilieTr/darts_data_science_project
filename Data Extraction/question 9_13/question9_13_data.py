from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd
import ast

# Dictionary to store tournament URLs and their respective match history pages
data = {}

# File path to the text file containing stored URLs
file_path = './Data Extraction/urls_flashcore.txt'

# Read the text file and store data in the dictionary
with open(file_path, "r", encoding="iso 8859-1") as file:
    for line in file:
        key, value = line.strip().split(':', 1)  # Split key and value
        data[key.strip()] = value.strip()

# Automatically download and use the correct WebDriver
service = Service(ChromeDriverManager().install())

for tournament, urls in data.items():
    data_df = []  # List to store extracted match data
    urls = ast.literal_eval(urls)  # Convert string representation of list to an actual list
    
    for url in urls:
        driver = webdriver.Chrome(service=service) 
        
        # Append '/spiel-historie' to access match history page
        url = url + '/spiel-historie'
        driver.get(url)

        # Wait until the page is fully loaded
        time.sleep(2)

        # Get page contents
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Extract player names
        players = soup.find_all(
            "div", 
            class_="participant__participantName"
        )
        players_text = []

        for player in players:
            players_text.append(player.find('a').get_text())

        # Find all divs with class 'matchHistoryRow' (score data)
        divs_first = soup.find_all('div', class_='matchHistoryRow')

        divs = []
        
        # Extract following divs with class 'matchHistoryRow__dartThrows' (dart throw history)
        for a in divs_first:
            b = a.find_next_sibling(
                'div', 
                class_='matchHistoryRow__dartThrows'
            )
            if b:
                divs.append((a.text, b.text))

        # Close the WebDriver to free up resources
        driver.quit()

        # Process extracted match history data
        for match in divs:
            score, coordinates = match
            
            # Split score into points and "VERLORENER ANWURF" (lost throw-in)
            if 'VERLORENER ANWURF' in score:
                if score.startswith('VERLORENER ANWURF'):
                    parts = score.split('VERLORENER ANWURF')
                    score_points = parts[1]
                    score_text = 'VERLORENER ANWURF Home'
                else:
                    parts = score.split('VERLORENER ANWURF')
                    score_points = parts[0]
                    score_text = 'VERLORENER ANWURF Away'
            else:
                score_points = score
                score_text = ''
            
            # Clean dart throw data and convert it into a list
            coordinate_list = [
                coord.replace("140+", "").replace("180", "") 
                for coord in coordinates.split(", ")
            ]
            
            legs = 0  # Initialize leg counter
            value_home = '501'  # Starting score for the home player
            value_away = '501'  # Starting score for the away player
            
            for value in coordinate_list:
                value = value.split(':')
                
                # Ensure valid values before processing
                if value[0] != '' and value[1] != '':
                    throw_home = int(value_home) - int(value[0])  # Points deducted for home player
                    throw_away = int(value_away) - int(value[1])  # Points deducted for away player
                    
                    # Update remaining scores
                    value_home = value[0]
                    value_away = value[1]
                    
                    # Store match data as a dictionary
                    row = {
                        'Leg': legs, 
                        'Leg Value': score_points, 
                        'Throw-in': score_text, 
                        'Value Home': value[0], 
                        'Value Away': value[1], 
                        'Throw Home': throw_home, 
                        'Throw Away': throw_away, 
                        'Player Home': players_text[0], 
                        'Player Away': players_text[1],
                    }
                    data_df.append(row)
                    print(row)
                    legs += 1  # Increment leg counter
            
        # Convert match data to a Pandas DataFrame
        df = pd.DataFrame(data_df)

        # Save extracted data as a CSV file
        df.to_csv(
            './Data/Flashcore/' + tournament.replace(" ", "_") + '.csv', 
            index=False
        )