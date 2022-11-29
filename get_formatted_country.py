import pandas as pd


def get_formatted_country(origin_string):
    return [x.strip() for x in origin_string.split(",")]


if __name__ == "__main__":
    billboard_artists_data = pd.read_csv("datasets/yearly/artists.csv")

    cities, states, countries = [], [], []
    for index in range(len(billboard_artists_data)):
        origin_string = billboard_artists_data.iloc[index, 2]
        city, state, country = None, None, None
        if not pd.isna(origin_string):
            origin_string = billboard_artists_data.iloc[index, 2]
            print(origin_string)
            city, state, country = get_formatted_country(origin_string)
        cities.append(city)
        states.append(state)
        countries.append(country)

    billboard_artists_data = billboard_artists_data.drop("origin", axis=1)

    billboard_artists_data['city'] = cities
    billboard_artists_data['state'] = states
    billboard_artists_data['country'] = countries

    print(billboard_artists_data)
    billboard_artists_data.to_csv("datasets/yearly/artists.csv", index=False)
