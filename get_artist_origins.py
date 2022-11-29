from bs4 import BeautifulSoup
import pandas as pd
import re
import wikipedia

wikipedia.set_lang("en")


def get_country(artist_name):
    print(f"Retriving {artist_name} origin...")
    origin = None

    try:
        results = wikipedia.search(artist_name)

        result_index = 0
        while origin is None and result_index < len(results):
            page_html = wikipedia.page(results[result_index], auto_suggest=False).html()
            soup = BeautifulSoup(page_html, 'html.parser')

            infobox = soup.find("table", class_="infobox")
            infobox_rows = infobox.find_all("tr") if infobox is not None else None
            for row in infobox_rows:
                origin_candidate = row.text
                # result = re.match("(.*)[0-9]{2}, [0-9]{4}(.*)", birthplace_candidate)
                if "Origin" in origin_candidate:
                    origin = origin_candidate.replace("Origin", "").rsplit(")")[-1]
                    break
            if origin is None:
                birthplace_div = soup.find("div", class_="birthplace")
                if birthplace_div is not None:
                    origin = birthplace_div.text
            if origin is None:
                for row in infobox_rows:
                    birthplace_candidate = row.text
                    if "Born" in birthplace_candidate:
                        origin = birthplace_candidate.replace("Born", "").rsplit(")")[-1]
                        break
            result_index += 1
    except:
        pass

    birthplace = re.sub("\[.*?\]", "", origin).strip() if origin is not None else origin
    return birthplace


if __name__ == "__main__":
    billboard_artists_data = pd.read_csv("datasets/billboard_yearly/artists.csv")
    for index in range(len(billboard_artists_data)):
        artist_name = billboard_artists_data.iloc[index, 1]
        origin = get_country(artist_name)
        print(origin)
        billboard_artists_data.iloc[index, 2] = origin
    billboard_artists_data.to_csv("datasets/billboard_yearly/artists.csv", index=False)
