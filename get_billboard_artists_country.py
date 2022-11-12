from bs4 import BeautifulSoup
import os
import pandas as pd
import wikipedia

wikipedia.set_lang("en")


def get_country(artist_name):
    os.system('clear' if os.name == 'posix' else 'cls')

    try:
        result = wikipedia.search(artist_name, results=1)[0]
        page_html = wikipedia.page(result, auto_suggest=False).html()
        soup = BeautifulSoup(page_html, 'html.parser')
        birthplace = soup.find("div", class_="birthplace")
        if birthplace is not None:
            birthplace = birthplace.text
            print(birthplace)
        else:
            infobox = soup.find("table", class_="infobox").text
            print(infobox)
            birthplace = input(f"Insert {artist_name} country: ")
    except Exception:
        birthplace = input(f"Insert {artist_name} country: ")

    parts = birthplace.split(",")
    while len(parts) != 3:
        parts = input(f"Insert {artist_name} country: ").split(",")

    return parts


if __name__ == "__main__":
    billboard_artists_data = pd.read_csv("datasets/billboard_artists.csv")
    for index in range(len(billboard_artists_data)):
        artist_name = billboard_artists_data.iloc[index, 1]
        p1, p2, p3 = get_country(artist_name)
        billboard_artists_data.iloc[index, 2] = p1
        billboard_artists_data.iloc[index, 3] = p2
        billboard_artists_data.iloc[index, 4] = p3
    billboard_artists_data.to_csv("datasets/billboard_artists_country.csv", index=False)
