from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pprint

Client_ID = ###
Client_Secret = ###

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
    scope  = "playlist-modify-private",
    client_id = Client_ID,
    client_secret = Client_Secret,
    redirect_uri = "http://example.com",
    show_dialog = True,
    cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

year = input("Which year would you like to travel to? (YYYY-MM-DD)")
webpage = requests.get("https://www.billboard.com/charts/hot-100/" + year)

soup = BeautifulSoup(webpage.text, "html.parser")

top_100_songs = soup.find_all(name="span", class_="chart-element__information__song")
song_names = [song_name.getText() for song_name in top_100_songs]

song_uris = []
year = year.split("-")[0]
for song in song_names:
    results = sp.search(q=song, type="track")
    # pprint.pprint(results)
    try:
        uri = results["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)
# print(playlist)

final = sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
# print(final)
