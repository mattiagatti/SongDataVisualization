import traceback

from bs4 import BeautifulSoup
import pandas as pd
import re
import wikipedia

wikipedia.set_lang("en")


def get_country(artist_name):
    print(f"Retriving {artist_name} birthplace...")
    birthplace = None

    try:
        result = wikipedia.search(artist_name, results=1)[0]
        page_html = wikipedia.page(result, auto_suggest=False).html()
        soup = BeautifulSoup(page_html, 'html.parser')
        birthplace_div = soup.find("div", class_="birthplace")
        if birthplace_div is not None:
            birthplace = birthplace_div.text
        else:
            infobox = soup.find("table", class_="infobox")
            infobox_rows = infobox.find_all("tr") if infobox is not None else None
            for row in infobox_rows:
                birthplace_candidate = row.text
                result = re.match("(.*)[0-9]{2}, [0-9]{4}(.*)", birthplace_candidate)
                if result:
                    birthplace = birthplace_candidate.rsplit(')', 1)[1]
                    break
    except:
        pass

    return re.sub("[\[].*?[\]]", "", birthplace).strip() if birthplace is not None else "not available"


if __name__ == "__main__":
    billboard_artists_data = pd.read_csv("datasets/billboard_artists.csv")
    for index in range(len(billboard_artists_data)):
        artist_name = billboard_artists_data.iloc[index, 1]
        birthplace = get_country(artist_name)
        print(birthplace)
        billboard_artists_data.iloc[index, 2] = birthplace
    billboard_artists_data.to_csv("datasets/billboard_artists.csv", index=False)
