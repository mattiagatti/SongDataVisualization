import pandas as pd

artists_path = "datasets/billboard_yearly/billboard_artists.csv"
associations_path = "datasets/billboard_yearly/billboard_song_artist_association.csv"
songs_path = "datasets/billboard_yearly/billboard_songs.csv"

df1 = pd.read_csv(artists_path)
df2 = pd.read_csv(associations_path)
df3 = pd.read_csv(songs_path)

merged = df1.merge(df2, on="artist_id").merge(df3, on="song_id")
merged = merged.sort_values("year")
data = merged.drop(["artist_name", "city_id", "rank", "song_id", "title"], axis=1)
artist_ids = sorted(data["artist_id"].unique())
first_year = data["year"].min()
last_year = data["year"].max() + 1
result = pd.DataFrame(columns=["artist_id", "cumulative_song_count", "year"])
for year in range(first_year, last_year, 1):
    print(year)
    data_filtered = data[data["year"] == year]
    for artist_id in artist_ids:
        count = result.loc[len(result) - len(artist_ids), "cumulative_song_count"] if year > first_year else 0
        for _, row in data_filtered.iterrows():
            if row["artist_id"] == artist_id:
                count += 1
        new_row = pd.DataFrame({"artist_id": [artist_id],
                                "cumulative_song_count": [count],
                                "year": [year]})
        result = pd.concat([result, new_row], ignore_index=True, axis=0)
result.to_csv("datasets/billboard_tableau_animation.csv", index=False)
