import pandas as pd

'''
def get_formatted_country(lat, lng):
    coordinates = f"{lat}, {lng}"
    print(f"Retriving {coordinates} address...")
    try:
        locator = Nominatim(user_agent="myGeocoder")
        location = locator.reverse(f"{coordinates}")
        address = location.raw["address"]
        parts = origin_string.split(",")

        if "city" in address:
            city = address["city"]
        elif "town" in address:
            city = address["town"]
        else:
            city = parts[0]

        country = address["country"]
        state = address["state"] if "state" in address else country

        country = "Ireland" if country == "Éire / Ireland" else country
        country = "Algeria" if country == "Algerian" else country
        country = "New Zealand" if country == "New Zealand / Aotearoa" else country
    except Exception:
        city, state, country = None, None, None

    print(city, state, country)
    return city, state, country
'''

def get_formatted_country(origin_string):
    return origin_string.split(",")

if __name__ == "__main__":
    billboard_artists_data = pd.read_csv("datasets/billboard_artists.csv")
    billboard_artists_data = billboard_artists_data.dropna()

    cities, states, countries = [], [], []
    for index in range(len(billboard_artists_data)):
        latitude = billboard_artists_data.iloc[index, 3]
        longitude = billboard_artists_data.iloc[index, 4]
        origin_string = billboard_artists_data.iloc[index, 2]
        city, state, country = get_formatted_country(origin_string)
        cities.append(city)
        states.append(state)
        countries.append(country)

    billboard_artists_data = billboard_artists_data.drop("origin", axis=1)
    billboard_artists_data = billboard_artists_data.drop("latitude", axis=1)
    billboard_artists_data = billboard_artists_data.drop("longitude", axis=1)

    billboard_artists_data['city'] = cities
    billboard_artists_data['state'] = states
    billboard_artists_data['country'] = countries

    billboard_artists_data.to_csv("datasets/billboard_artists_formatted.csv", index=False)
