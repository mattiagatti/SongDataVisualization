from geopy import Nominatim
import pandas as pd


def get_latlng(origin_string):
    latitude, longitude = None, None
    print(f"Retriving {origin_string} latitude and longitude...")
    if not pd.isna(origin_string):
        try:
            locator = Nominatim(user_agent="myGeocoder")
            location = locator.geocode(origin_string)
            latitude, longitude = location.latitude, location.longitude
        except:
            pass
    print(latitude, longitude)
    return latitude, longitude


if __name__ == "__main__":
    billboard_artists_data = pd.read_csv("datasets/billboard_artists.csv")

    billboard_artists_data["origin"] = billboard_artists_data["origin"].apply(
        lambda x: x.replace("U.S.", "United States") if not pd.isna(x) else x)
    billboard_artists_data["origin"] = billboard_artists_data["origin"].apply(
        lambda x: x.replace("U.K.", "United Kingdom") if not pd.isna(x) else x)

    billboard_artists_data.insert(3, "latitude", None)
    billboard_artists_data.insert(4, "longitude", None)

    for index in range(len(billboard_artists_data)):
        origin_string = billboard_artists_data.iloc[index, 2]
        latitude, longitude = get_latlng(origin_string)
        billboard_artists_data.iloc[index, 3] = latitude
        billboard_artists_data.iloc[index, 4] = longitude
    billboard_artists_data.to_csv("datasets/billboard_artists.csv", index=False)
