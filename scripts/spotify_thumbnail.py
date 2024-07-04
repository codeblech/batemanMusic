import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

import os
import requests
from io import BytesIO
from PIL import Image

load_dotenv()

def get_spotify_thumbnail(url: str) -> None | str:
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    result = spotify.track(url)

    thumbnail_url = result["album"]["images"][0]["url"]
    id = result["album"]["artists"][0]["id"]
    print(id)
    save_name = id
    save_path = os.path.join("./assets/thumbnails/spotify", f"{save_name}.jpg")
    os.makedirs("./assets/thumbnails/spotify", exist_ok=True)

    # check if this thumbnail is already available, and return it if it exists
    try:
        with open(save_path) as im:
            print("using already generated spotify thumbnail")
        return save_path
    except:
        pass

    rr = requests.get(thumbnail_url)
    if rr.status_code != 200:
        return None
    with Image.open(BytesIO(rr.content)) as im:
        try:
            im.save(save_path, format="JPEG")
            return save_path
        except:
            return None


if __name__ == "__main__":
    get_spotify_thumbnail("https://open.spotify.com/track/1gqkRc9WtOpnGIqxf2Hvzr?si=bd0351766c9b496f")
