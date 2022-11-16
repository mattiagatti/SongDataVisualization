from geopy import Nominatim
import pandas as pd

def get_formatted_country(lat, lng):
    try:
        locator = Nominatim(user_agent="myGeocoder")
        location = locator.reverse(f"{lat}, {lng}")
        address = location.raw["address"]
        print(address)
        city = address["city"] if "city" in address else address["town"]
        state, country = address["state"], address["country"]
    except:
        city, state, country = None, None, None
    return city, state, country


if __name__ == "__main__":
    billboard_artists_data = pd.read_csv("datasets/billboard_artists.csv")
    cities, states, countries = [], [], []

    for index in range(len(billboard_artists_data)):
        latitude = billboard_artists_data.iloc[index, 3]
        longitude = billboard_artists_data.iloc[index, 4]
        city, country, state = get_formatted_country(latitude, longitude)
        cities.append(city)
        states.append(state)
        countries.append(country)
        billboard_artists_data.iloc[index, 3] = latitude
        billboard_artists_data.iloc[index, 4] = longitude

    billboard_artists_data.drop("origin", axis=1)
    billboard_artists_data.drop("latitude", axis=1)
    billboard_artists_data.drop("longitude", axis=1)

    billboard_artists_data['city'] = cities
    billboard_artists_data['state'] = states
    billboard_artists_data['country'] = countries

    billboard_artists_data.to_csv("datasets/billboard_artists_formatted.csv", index=False)