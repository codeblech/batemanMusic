# thumbnail xpath: //*[@id="img"]
# thumbnail full xpath: /html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-page/div/div[1]/ytmusic-player/div[1]/yt-img-shadow/img
# next step: robustness. add code to handle when ytmusc doesnt return deprecation warning.
# more meaning error handling
# make the filename unique using other metadata
# handle the landscape style thumbnails. maybe crop the bateman video according to the thumbnail. maybe keep a few versions of the bateman video ready
# check if thumbnail for this song is already there (downloaded)
# use logging module
# use uv package manager
# feature: add crop capability for thumbnail
# temporarily handle different resolutions by cropping

# uploaded image crop: allow any range between original ratio of bateman_original.mp4 and 1:1
# according to the thumbnail, crop the bateman_original.mp4
# for youtube, keep it frinctionless: use bateman_original.mp4
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
        thumbnail_url = meta.get("content", None)

    if thumbnail_url is not None:
        rr = requests.get(thumbnail_url)
        if rr.status_code != 200:
            return None
        save_name = regex.findall(".*=(.*)", url)[0]  # extract last part of url

        os.makedirs("./assets/thumbnails/ytmusic", exist_ok=True)
        save_path = os.path.join("./assets/thumbnails/ytmusic", f"{save_name}.jpg")
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
