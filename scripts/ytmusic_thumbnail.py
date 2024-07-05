# next step: robustness. add code to handle when ytmusc doesnt return deprecation warning.
# more meaningful error handling
# make the filename unique and predictable using better regex to get video id in ytmusic
# check if thumbnail for this song is already there (downloaded)
# use logging module
# use uv package manager

# avoid re-rendering of site on using slider
# give a key to every slider, embed button, audio and video element to make them unique
# add music to youtube music videos
# yt_dlp doesn't work on hosted site
# make a single input box that detects what platform link is pasted


from bs4 import BeautifulSoup
import requests
import os
from PIL import Image
from io import BytesIO
import regex


def get_ytmusic_thumbnail(url: str) -> str | None:
    """Get the thumbnail of a song, playlist, or album using its youtube music url

    Args:
        link (str): YouTube Music url to the song

    Returns:
        str | None: path to the downloaded thumbail image file
    """
    r = requests.get(url)
    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.content, "lxml")
    # print(f"soup: {soup.prettify()}")
    title_tags = soup.find_all("title") # ytmusic returns two title tags in html

    if "Your browser is deprecated" in str(title_tags[0]):
        meta = soup.find("meta", {"property": "og:image"})
        thumbnail_url = meta.get("content", None)

    if thumbnail_url is not None:
        rr = requests.get(thumbnail_url)
        if rr.status_code != 200:
            return None

        save_name = regex.findall(r".*=(.*)", url)[0]  # extract last part of url
        save_path = os.path.join("./assets/thumbnails/ytmusic", f"{save_name}.jpg")
        os.makedirs("./assets/thumbnails/ytmusic", exist_ok=True)

        with Image.open(BytesIO(rr.content)) as im:
            try:
                im.save(save_path, format="JPEG")
                return save_path
            except:
                return None


if __name__ == "__main__":
    get_ytmusic_thumbnail(
        "https://music.youtube.com/watch?v=qjnn00I9t4I&si=8EyUorifYtMbV7Sz"
    )
