import sys
import os
import time
import ast
import pandas as pd
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import get_driver

def load_urls(file_path):
    """
    Reads tournament URLs from a text file into a dictionary.
    """
    url_data = {}
    with open(file_path, "r", encoding="iso 8859-1") as file:
        for line in file:
            key, value = line.strip().split(':', 1)
            url_data[key.strip()] = value.strip()
    return url_data

def get_match_history(url, driver):
    """
    Fetches and parses the match history page.
    """
    driver.get(url + '/spiel-historie')
    time.sleep(2)  # Ensure the page fully loads
    return BeautifulSoup(driver.page_source, 'html.parser')

def extract_players(soup):
    """
    Extracts player names from the match history page.
    """
    return [player.find('a').get_text() 
            for player in soup.find_all(
                "div", class_="participant__participantName"
            )
        ]

def extract_scores(soup):
    """
    Extracts match history scores and dart throws.
    """
    match_data = []
    score_divs = soup.find_all('div', class_='matchHistoryRow')
    for div in score_divs:
        dart_throws = div.find_next_sibling('div', class_='matchHistoryRow__dartThrows')
        if dart_throws:
            match_data.append((div.text, dart_throws.text))
    return match_data

def process_match_data(players, match_data):
    """
    Processes and structures match data for DataFrame conversion.
    """
    data_df = []
    for score, coordinates in match_data:
        score_text, score_points = (
            "Lost Throw-in Home", 
            score.split('VERLORENER ANWURF')[1]
        ) if 'VERLORENER ANWURF' in score else ("", score)
        coordinate_list = [
            coord.replace("140+", "").replace("180", "") 
            for coord in coordinates.split(", ")
        ]
        legs, value_home, value_away = 0, '501', '501'
        for value in coordinate_list:
            home, away = value.split(':')
            if home and away:
                row = {
                    'Leg': legs,
                    'Leg Value': score_points,
                    'Throw-in': score_text,
                    'Value Home': home,
                    'Value Away': away,
                    'Throw Home': int(value_home) - int(home),
                    'Throw Away': int(value_away) - int(away),
                    'Player Home': players[0],
                    'Player Away': players[1]
                }
                data_df.append(row)
                legs += 1
                value_home, value_away = home, away

    return pd.DataFrame(data_df)

def save_to_csv(df, tournament_name):
    """
    Saves DataFrame to a CSV file.
    """
    df.to_csv(f'./Data/flashcore/{tournament_name.replace(" ", "_")}.csv', index=False)

def main():
    """
    Main function.
    """
    file_path = './Data_Extraction/Flashcore/urls_flashcore.txt'
    tournaments = load_urls(file_path)
    
    for tournament, urls in tournaments.items():
        urls = ast.literal_eval(urls)
        all_matches = []
        
        for url in urls:
            driver = get_driver()
            soup = get_match_history(url, driver)
            driver.quit()
            
            players = extract_players(soup)
            match_data = extract_scores(soup)
            df = process_match_data(players, match_data)
            all_matches.append(df)
        
        final_df = pd.concat(all_matches, ignore_index=True)
        save_to_csv(final_df, tournament)
        
if __name__ == "__main__":
    main()
