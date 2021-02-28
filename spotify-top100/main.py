## This program will ask a user for a date (YYYY-MM-DD)
## It will then scrape billboard.com's hot-100 chart for the specific date
## Finally it will use the Spotify API and create a private playlist of the hot-100 list.

from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import datetime
import os

# Request date from user
URL = "https://billboard.com/charts/hot-100/"
user_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = datetime.datetime.strptime(user_date, "%Y-%m-%d").year


SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET = os.getenv("SPOTIFY_SECRET")
REDIRECT_URL = "http://example.com"

# Use BeautifulSoup to parse the html and compile separate lists for songs and artists
response = requests.get(f"{URL}{user_date}")
soup = BeautifulSoup(response.text, "html.parser")
list_of_songs_html = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
list_of_songs = [song.getText() for song in list_of_songs_html]
list_of_artists_html = soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")
list_of_artists = [artist.getText() for artist in list_of_artists_html]


# Create a spotify object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_SECRET,
                                               redirect_uri=REDIRECT_URL,
                                               scope="playlist-modify-private",
                                               show_dialog=True))

user_id = sp.current_user()["id"]

# Create a new list of spotify URIs by searching for the songs in the previously made list
uri_list = []
for song in list_of_songs:
    result = sp.search(q=f'track: {song}: {year}', type='track', limit=1)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uri_list.append(uri)
    except IndexError:
        print(f"{song} not found in Spotify. Skipped. ")


# Create an empty private playlist
playlist = sp.user_playlist_create(user_id, f"{user_date} Billboard 100", public=False, collaborative=False, description=f"Billboards top 100 songs for the date {user_date}")
print(playlist)

# Add songs to the playlist
sp.playlist_add_items(playlist["id"], uri_list)

