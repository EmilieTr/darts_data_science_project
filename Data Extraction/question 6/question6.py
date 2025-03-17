import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


def exceptions(word):
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
    # Split the name into individual words
    parts = full_name.split()
    if len(parts) < 2:
        return full_name  # If only one name exists, return unchanged

    # First letter of the first name + period
    first_name_initial = parts[0][0] + "."
    # Everything except the first word as last name
    last_name = " ".join(parts[1:])

    return f"{last_name} {first_name_initial}"


def extract_name(txt):
    x = 0
    y = 0
    name_list = []
    real_name = ''
    # When we have a hyphen that belongs to the name, case = True
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
            name = exceptions(name)
            name_list.append(name)
            y = x + 1
            x += 1
        else:
            case = False
            x += 1


def list_of_names(url):
    # Accessing the website
    response = requests.get(url)

    if response.status_code == 200:
        # Parsing the HTML-Codes
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
            if player_name is not None:
                player_names.append(player_name)
            player = player.find_next('li')

    else:  # If website is not found, turn back error message
        print(f"Error: {response.status_code}")

    return player_names


def name_format_url(lst):
    name = ''
    new_list = lst[:len(lst) - 1]
    for i in new_list:
        name = name + i + '_'
    return name[:len(name) - 1], lst[len(lst) - 1]


# URL of the website, with a list of all darts players
# List of all men
url = 'https://www.dartn.de/Dart-Profis'
# List of all women
# url = 'https://www.dartn.de/Dart-Profis_Damen'

# List of all darts players
list_players = list_of_names(url)
# print(list_players_men)
data_list = []
error_list = []

# Create matching URL for all players
for name in list_players:
    name_url, real_name = name_format_url(name)
    # print(name_url, real_name)
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
                    # Extract text from found <p> tag
                    text = fact.text

                    # Regular expressions for desired information
                    pattern = {
                        "Geburtstag": r"Geburtstag:\s*([\d\w\.\-]*)\s*Geburtsort",
                        "Plays since": r"Spielt Dart seit:\s*([-\w\s]*)\s*Profi seit",
                        "Profi since": r"Profi seit:\s*([-\w\s]*)\s*Händigkeit",
                        "Nationality": r"Nationalität:\s*([\w\s]+)\s*Familienstand",
                        "Handedness": r"Händigkeit:\s*([\w\s]+)Darts",
                        "Darts gramm": r"Darts:\s*([-\w\s]*)\s*Sponsoren",
                    }

                    # Extract results
                    data = {
                        key: re.search(pattern[key], text).group(1).strip() 
                        if re.search(pattern[key], text) else None 
                        for key in pattern
                    }
                    # Replace "-" with None
                    data = {
                        key: (None if value == "-" else value) 
                        for key, value in data.items()
                    }

                    data['Name'] = real_name
                    formatted_name = format_name(real_name)
                    data["Name S."] = formatted_name
                                
                    data_list.append(data)
            else: 
                facts = facts.find_next('h2')
            
    else:  # If website is not found, turn back error message
        error = {}
        error['player'] = name
        error['error'] = {response.status_code}
        error_list.append(error)
        print(error)
        # print(f"Error: {response.status_code}", name)

# Create a pandas dataframe
df = pd.DataFrame(data_list)
dferror = pd.DataFrame(error_list)

# Print first 5 lines of the data frame
# print(df.head())

# Saving as a csv file
df.to_csv("./Data/players/male_players2.csv", index=False)
dferror.to_csv("./Data/players/error_male_players2.csv", index=False)

# Saving as a csv file woman
# df.to_csv("./Data/question 6/woman_players.csv", index=False)
# dferror.to_csv("./Data/question 6/error_woman_players.csv", index=False)