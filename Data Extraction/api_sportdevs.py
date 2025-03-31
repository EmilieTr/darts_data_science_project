import requests
import pandas as pd

urls = ["leagues", "tournaments", "countries", "teams", "matches", "arenas", "seasons", "standings"]
payload = {}
dfs = {}
headers = {
    'Authorization': 'Bearer YZfp_fpMoE2iKvzjA4djJg'
}

for url in urls:
    whole_url = "https://darts.sportdevs.com/" + url
    response = requests.request("GET", whole_url, headers=headers, data=payload)
    # Convert JSON response to Python data structure
    data = response.json()
    # If data contains a list of dictionaries (e.g. [{"name": "A", "value": 10}, ...])
    df = pd.DataFrame(data)
    # df = pd.concat(response, ignore_index=True)
    df.to_csv("./Data/api_sportdevs/" + url + ".csv", index=False, encoding="utf-8")

# print(response.text)