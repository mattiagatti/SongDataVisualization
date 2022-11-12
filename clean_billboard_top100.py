import pandas as pd


def replace_all(artist):
    # these two needs to be handled directly
    if not any(x in artist for x in ("X Ambassador", "Lil Nas X")):
        artist = artist.replace(" X ", "&")

    # and also these
    artist = artist.replace("+", "and") if "Dan + Shay" in artist else artist
    artist = artist.replace("Jay Z", "Jay-Z") if "Jay Z" in artist else artist
    artist = "Bruno Mars & Anderson.Paak" if "Silk Sonic" in artist else artist
    artist = "Dirty Money" if artist == "Diddy - Dirty Money" else artist

    connectors = ("(Featuring", "Featuring", "Feat.", "Duet With", " With ",
                  " / ", " + ", " Or ", " (", " x ", ", &", ", ")
    for connector in connectors:
        artist = artist.replace(connector, "&").replace(")", "")

    return artist


def divide_artists(billboard_data):
    artists = billboard_data["artist"]

    divided = []
    for artist in artists:
        single_artists = artist.split("&")
        single_artists = [x.strip() for x in single_artists]
        divided += single_artists

    result = list(set(divided))
    return sorted(result, key=str.casefold)


def get_associations(billboard_data, artists_data):
    associations = []
    for song_id, row in billboard_data.iterrows():
        single_artists = row["artist"].split("&")
        single_artists = [x.strip() for x in single_artists]
        for single_artist in single_artists:
            artist_row = artists_data.loc[artists_data["name"] == single_artist]
            artist_id = artist_row.index[0]
            associations.append((song_id, artist_id))

    return associations


if __name__ == "__main__":
    billboard_data = pd.read_csv("scraps/billboard_scraps.csv")
    billboard_data["artist"] = billboard_data["artist"].apply(lambda x: replace_all(x))

    artists = divide_artists(billboard_data)
    d = {'name': artists, 'city': None, 'region': None, 'state': None}
    artists_data = pd.DataFrame(data=d)
    artists_data.index.name = 'artist_id'
    artists_data.to_csv("datasets/billboard_artists.csv")

    associations = get_associations(billboard_data, artists_data)
    associations_data = pd.DataFrame(columns=['fk_song', 'fk_artist'], data=associations)
    associations_data.to_csv("datasets/billboard_song_artist_association.csv", index=False)

    billboard_data = billboard_data.drop("artist", axis=1)
    billboard_data.to_csv("datasets/billboard_songs.csv", index=False)
