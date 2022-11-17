import pandas as pd


def replace_all(artist):
    # these two needs to be handled directly
    if not any(x in artist for x in ("X Ambassador", "Lil Nas X")):
        artist = artist.replace(" X ", "&")

    # and also these
    artist = artist.replace("+", "and") if "Dan + Shay" in artist else artist
    artist = artist.replace("Diddy - Dirty Money", "Diddy") if "Diddy - Dirty Money" in artist else artist
    artist = artist.replace("Kesha", "Ke$ha") if "Kesha" in artist else artist
    artist = artist.replace("WizKid", "Wizkid") if "WizKid" in artist else artist
    artist = artist.replace("Young D", "Yung D") if "Young D " in artist else artist
    artist = artist.replace("Ayo & Teo", "Ayo and Teo") if "Ayo & Teo" in artist else artist
    artist = artist.replace("THE SCOTTS,", "") if "THE SCOTTS," in artist else artist
    artist = artist.replace("&", "and") if "Mumford & Sons" in artist else artist
    artist = artist.replace("&", "and") if "Nico & Vinz" in artist else artist
    artist = artist.replace("The Throne", "Kanye West Featuring Jay-Z") if "The Throne" in artist else artist

    artist = artist.replace("Jay Z", "Jay-Z").replace("JAY Z", "Jay-Z") \
        if "Jay Z" in artist or "JAY Z" in artist else artist
    artist = artist.replace("Sean Paul Of The YoungBloodZ", "Sean Paul") \
        if "Sean Paul Of The YoungBloodZ" in artist else artist
    artist = artist.replace("Soulja Boy Tell'em", "Soulja Boy").replace("Soulja Boy Tell 'em", "Soulja Boy") \
        if "Soulja Boy Tell'em" in artist or "Soulja Boy Tell 'em" in artist else artist

    artist = "Jay-Z Featuring Kanye West" if artist == "Jay-Z Kanye West" else artist
    artist = "Bruno Mars & Anderson .Paak" if "Silk Sonic" in artist else artist

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
    d = {'name': artists, 'origin': None}
    artists_data = pd.DataFrame(data=d)
    artists_data.index.name = 'artist_id'
    artists_data.to_csv("datasets/billboard_artists.csv")

    associations = get_associations(billboard_data, artists_data)
    associations_data = pd.DataFrame(columns=['song_id', 'artist_id'], data=associations)
    associations_data.to_csv("datasets/billboard_song_artist_association.csv", index=False)

    billboard_data = billboard_data.drop("artist", axis=1)
    billboard_data.to_csv("datasets/billboard_songs.csv", index=False)
