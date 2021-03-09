import os 
from bs4 import BeautifulSoup
import requests



# Environ.. loading
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET =  os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_ACCESS_TOKEN = os.environ.get("SPOTIFY_ACCESS_TOKEN")
SPOTIFY_USER_ID = os.environ.get("SPOTIFY_USER_ID")


# Setup

headers = {
    "Authorization" : f"Bearer {SPOTIFY_ACCESS_TOKEN}"
}



# Input Playlist Name
playlist_name = input("Name of the playlist : ")

# Scrapping
print("Scrapping songs...")
url = "https://www.billboard.com/charts/hot-100/2021-02-20"
response = requests.get(url= url)
soup = BeautifulSoup(response.text, "html.parser")
songs = soup.select("span.chart-element__information__song.text--truncate.color--primary")
songs_list = [item.getText() for item in songs]


# Search track
print("Fetching songs uri...")
tracks_uri = []
for song in songs_list:

    req_params = {
        "q": song, 
        "type":"track",
        "limit":"1"
    }

    response = requests.get(url="https://api.spotify.com/v1/search", params=req_params, headers=headers)
    response = response.json()
    try:
        track_uri = response["tracks"]["items"][0]["uri"]
    except KeyError:
        print(f"{song} > Missing", end="\n")
    else:
        print(f"{song} > {track_uri}",end="\n")
        tracks_uri.append(track_uri)

# tracks_uri_str= tracks_uri.join(",")



print("Creating Playlist...")
# # Create a Playlist 
response = requests.post(url=f"https://api.spotify.com/v1/users/{SPOTIFY_USER_ID}/playlists", json={"name":{playlist_name}},headers=headers)
playlist_data = response.json()
playlist_id = playlist_data["id"]


# Add songs into the playlist
print("Adding songs into the Playlist...") 
response = requests.post(url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers, json={ "uris":tracks_uri})
response = response.json()
print(response)


print(f"Link to play : http://open.spotify.com/user/{SPOTIFY_USER_ID}/playlists/{playlist_id}")