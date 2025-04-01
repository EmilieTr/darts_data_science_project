import os
import sys
import time
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import get_driver

def get_tournament_urls():
    """Returns a list of tournament URLs for major and European Tour events."""
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
    european_tour = [
        f"https://www.flashscore.de/dart/europa/european-tour-{num}/ergebnisse/" 
        for num in range(1, 14)
    ]
    return majors + european_tour

def extract_match_links(driver, urls):
    """Extracts match links for each tournament and returns a dictionary."""
    tournament_links = {}
    
    for url in urls:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = [
            a['href'] for a in soup.find_all(
                'a', href=lambda href: href and href.endswith('spiel-zusammenfassung')
            )
        ]
        tournament = url.split('/')[-3].replace('-', ' ')
        tournament_links[tournament] = links
    
    return tournament_links

def save_links_to_file(tournament_links, file_path):
    """Saves the extracted tournament links to a text file."""
    with open(file_path, 'w', encoding="iso 8859-1") as file:
        for tournament, links in tournament_links.items():
            file.write(f'{tournament}: {links}\n')

def main():
    file_path = './Data_Extraction/urls_flashcore.txt'
    urls = get_tournament_urls()
    driver = get_driver()
    tournament_links = extract_match_links(driver, urls)
    driver.quit()
    save_links_to_file(tournament_links, file_path)
    
if __name__ == "__main__":
    main()
