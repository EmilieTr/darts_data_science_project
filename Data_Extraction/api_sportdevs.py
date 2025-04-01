import requests
import pandas as pd

def fetch_data_from_api(url: str, headers: dict, payload: dict) -> pd.DataFrame:
    """
    Fetch data from the API and return it as a DataFrame.
    """
    full_url = f"https://darts.sportdevs.com/{url}"
    response = requests.get(full_url, headers=headers, data=payload)
    data = response.json()
    return pd.DataFrame(data)

def save_data_to_csv(df: pd.DataFrame, filename: str):
    """
    Save the DataFrame to a CSV file.
    """
    df.to_csv(filename, index=False, encoding="utf-8")

def main():
    urls = ["leagues", "tournaments", "countries", "teams", "matches", "arenas", "seasons", "standings"]
    payload = {}
    headers = {
        'Authorization': 'Bearer YZfp_fpMoE2iKvzjA4djJg'
    }

    for url in urls:
        df = fetch_data_from_api(url, headers, payload)
        save_data_to_csv(df, f"./Data/api_sportdevs/{url}.csv")

if __name__ == "__main__":
    main()
