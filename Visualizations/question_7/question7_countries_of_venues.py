import pandas as pd
from geopy.geocoders import Nominatim
import time

def countries_of_venues():
    """
    Process venue data from CSV files and extract countries for each venue.
    Saves the processed data to a new CSV file.
    """
    # Read CSV files
    df1 = pd.read_csv("./Data/host_country_nationality/host_country_nationality_majors.csv")
    df2 = pd.read_csv("./Data/host_country_nationality/host_country_nationality_european_tour.csv")

    df = pd.concat([df1, df2], ignore_index=True)

    # Initialize geocoder
    geolocator = Nominatim(user_agent="geo_finder")

    def get_country(city):
        """
        Determine the country for a given city using geopy."
        """
        try:
            location = geolocator.geocode(city, language='en')
            if location:
                return location.address.split(",")[-1].strip()
        except:
            return None
        return None

    # Extract city from venue location
    df['Stadt'] = df['Austragungsort'].apply(
        lambda x: x.split(",")[-1].strip() if isinstance(x, str) else None
    )

    # Determine countries for each city
    df['Austragungsland'] = df['Stadt'].apply(
        lambda city: get_country(city) if pd.notna(city) else None
    )

    # Delay between requests to respect API limits
    time.sleep(1)
    
    df.to_csv(
        "Visualizations/question_7/host_country_nationality_countries_to_venues.csv",
        index=True
    )

countries_of_venues()