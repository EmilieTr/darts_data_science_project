import requests
import pandas as pd
from bs4 import BeautifulSoup

def handle_exceptions(word):
    """Handle exceptions for character normalization."""
    word = word.replace('\xa0', '').replace("'", "").replace('.', '')
    word = word.replace('-\xa0', '')
    word = word.replace('á', 'a').replace('à', 'a').replace('â', 'a')
    word = word.replace('ó', 'o').replace('ò', 'o').replace('ô', 'o')
    word = word.replace('í', 'i').replace('ì', 'i').replace('î', 'i')
    word = word.replace('é', 'e').replace('è', 'e').replace('ê', 'e')
    word = word.replace('ß', 'ss').replace('ć', 'c').replace('ø', 'o')
    word = word.replace('ö', 'oe').replace('ü', 'ue').replace('ä', 'ae')
    word = word.replace('Ö', 'Oe').replace('Ü', 'Ue').replace('Ä', 'Ae')
    return word


def format_name(full_name):
    """Format name to match with other tables."""
    parts = full_name.split()
    if len(parts) < 2:
        return full_name

    first_name_initial = parts[0][0] + "."
    last_name = " ".join(parts[1:])

    return f"{last_name} {first_name_initial}"


def extract_name(txt):
    """
    Extract name from text containing additional information.
    """
    x = 0
    y = 0
    name_list = []
    real_name = ''
    case = False
    for i in txt:
        if i == '-' or i == '(' or i == '"':
            if i == '-':
                case = True
                x += 1
            else:
                name_list.append(real_name[1:])
                return name_list
        elif i == ' ':
            if case:
                name_list.append(real_name[1:])
                return name_list
            name = txt[y:x]
            real_name = real_name + ' ' + name
            name = handle_exceptions(name)
            name_list.append(name)
            y = x + 1
            x += 1
        else:
            case = False
            x += 1


def get_player_names(url):
    """
    Get list of all player names from the website.
    """
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        players = soup.find(
            'div',
            {'class': 'col-lg-9 col-md-8 col-sm-12 col-xs-12'}
        )
        player_names = []
        player = players.find_next('li')
        
        while player:
            player_name = player.text.strip()
            player_name = extract_name(player_name)
            if player_name:
                player_names.append(player_name)
            player = player.find_next('li')
    else:
        print(f"Error: {response.status_code}")
        return []

    return player_names


def create_url_name(lst):
    """
    Format name for URL construction.
    """
    name = ''
    new_list = lst[:-1]
    for i in new_list:
        name += i + '_'
    return name.rstrip('_'), lst[-1]


def extract_player_info(text, pattern):
    """
    Extract player information based on the provided patterns.
    """
    data = {}

    for key, search_string in pattern.items():
        start_index = text.find(search_string)
        
        if start_index != -1:
            start_index += len(search_string)
            end_index = text.find("\n", start_index)
            
            if end_index == -1:
                end_index = len(text)
            
            data[key] = text[start_index:end_index].strip()
        else:
            data[key] = None

    return data


def main():
    # URL of the website with list of all darts players
    url = 'https://www.dartn.de/Dart-Profis'
    # Alternative URL for women darts players
    # url = 'https://www.dartn.de/Dart-Profis_Damen'

    # Get list of all darts players
    player_list = get_player_names(url)

    data_list = []  # List with information of every player
    error_list = []  # List with names of players we can't get the information from

    # Create URL for all players and extract information
    for name in player_list:
        name_url, real_name = create_url_name(name)

        url_2 = f'https://www.dartn.de/{name_url}'

        response = requests.get(url_2)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            facts = soup.find('h2')
            
            while facts:
                if facts.text.strip() == 'Fakten zur Person:':
                    fact = facts.find_next('p')
                    facts = None
                    
                    if fact:
                        text = fact.text

                        # Information to extract
                        pattern = {
                            "Birthday": r"Geburtstag:\s*([\d\w\.\-]*)\s*Geburtsort",
                            "Plays since": r"Spielt Dart seit:\s*([-\w\s]*)\s*Profi seit",
                            "Profi since": r"Profi seit:\s*([-\w\s]*)\s*Händigkeit",
                            "Nationality": r"Nationalität:\s*([\w\s]+)\s*Familienstand",
                            "Handedness": r"Händigkeit:\s*([\w\s]+)Darts",
                            "Darts weight": r"Darts:\s*([-\w\s]*)\s*Sponsoren",
                        }

                        # Extract results
                        player_data = extract_player_info(text, pattern)
                        
                        # Replace "-" with None
                        player_data = {key: (None if value == "-" else value) for key, 
                                       value in player_data.items()
                                    }

                        # Add player name to the data
                        player_data['Name'] = real_name
                        formatted_name = format_name(real_name)
                        player_data["Formatted Name"] = formatted_name
                                    
                        data_list.append(player_data)
                else: 
                    facts = facts.find_next('h2')
        else:
            error = {}
            error['player'] = name
            error['error'] = {response.status_code}
            error_list.append(error)

    # Create pandas dataframes for data and errors
    df = pd.DataFrame(data_list)
    df_error = pd.DataFrame(error_list)

    # Saving as CSV files
    # df.to_csv("./Data/players/male_players2.csv", index=False)
    # df_error.to_csv("./Data/players/error_male_players2.csv", index=False)

    # For women players
    # df.to_csv("./Data/player_data/woman_players.csv", index=False)
    # df_error.to_csv("./Data/player_data/error_woman_players.csv", index=False)


# Execute the main function
if __name__ == "__main__":
    main()
