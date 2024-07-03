# thumbnail xpath: //*[@id="img"]
# thumbnail full xpath: /html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-page/div/div[1]/ytmusic-player/div[1]/yt-img-shadow/img
# next step: robustness. add code to handle when ytmusc doesnt return deprecation warning.
# more meaning error handling
# make the filename unique using other metadata
# handle the landscape style thumbnails. maybe crop the bateman video according to the thumbnail. maybe keep a few versions of the bateman video ready
# check if thumbnail for this song is already there (downloaded)
# use logging module
# use uv package manager
from bs4 import BeautifulSoup
import requests
import os
from PIL import Image
from io import BytesIO
import regex


def get_ytmusic_thumbnail(url: str) -> str | None:
    """Get the thumbnail of a song using its youtube music url

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
        image_link = meta.get("content", None)

    if image_link is not None:
        rr = requests.get(image_link)
        if rr.status_code != 200:
            return None
        save_name = regex.findall(".*=(.*)", url)[0]  # extract last part of url

        os.makedirs("./assets/thumbnails", exist_ok=True)
        save_path = os.path.join("./assets/thumbnails", f"{save_name}.jpg")
        with Image.open(BytesIO(rr.content)) as im:
            try:
                im.save(save_path, format="JPEG")
                return save_path
            except:
                return None


get_ytmusic_thumbnail(
    "https://music.youtube.com/watch?v=vQ0u09mFodw&list=PLe1TEKS7ZJ1n4ha8ILgKQHwSOz7TedObD"
)
