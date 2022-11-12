from bs4 import BeautifulSoup
import pandas as pd
import requests


def scrap(year):
    songs = []
    url = f"https://www.billboard.com/charts/year-end/{year}/hot-100-songs/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    boxes = soup.find_all("li", class_="lrv-u-width-100p")
    for i, box in enumerate(boxes):
        title = box.find("h3").text.strip()
        artist = box.find("span").text.strip()
        rank = i + 1
        songs.append((title, artist, rank, year))
    return songs


if __name__ == "__main__":
    data = []
    for year in range(2006, 2022):
        data += scrap(year)
    df = pd.DataFrame(data, columns=["title", "artist", "rank", "year"])
    df.index.name = 'song_id'
    df.to_csv("scraps/billboard_scraps.csv")
