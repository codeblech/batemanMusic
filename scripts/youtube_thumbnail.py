import requests
from PIL import Image
import os
from io import BytesIO
import re


# this function is taken from https://gist.github.com/rodrigoborgesdeoliveira/987683cfbfcc8d800192da1e73adc486?permalink_comment_id=5097394#gistcomment-5097394
def get_youtube_video_id_by_url(url):
    regex = r"^((https?://(?:www\.)?(?:m\.)?youtube\.com))/((?:oembed\?url=https?%3A//(?:www\.)youtube.com/watch\?(?:v%3D)(?P<video_id_1>[\w\-]{10,20})&format=json)|(?:attribution_link\?a=.*watch(?:%3Fv%3D|%3Fv%3D)(?P<video_id_2>[\w\-]{10,20}))(?:%26feature.*))|(https?:)?(\/\/)?((www\.|m\.)?youtube(-nocookie)?\.com\/((watch)?\?(app=desktop&)?(feature=\w*&)?v=|embed\/|v\/|e\/)|youtu\.be\/)(?P<video_id_3>[\w\-]{10,20})"
    match = re.match(regex, url, re.IGNORECASE)
    if match:
        return (
            match.group("video_id_1")
            or match.group("video_id_2")
            or match.group("video_id_3")
        )
    else:
        return None


def get_yt_thumbnail(url: str) -> None | str:
    """Get the thumbnail of a song using its youtube music url

    Args:
        url (str): YouTube url to the song

    Returns:
        str | None: path to the downloaded thumbail image file
    """
    video_id: str = get_youtube_video_id_by_url(url)
    thumbnail_url: str = "https://img.youtube.com/vi/" + video_id + "/maxresdefault.jpg"

    if thumbnail_url is not None:
        rr = requests.get(thumbnail_url)
        if rr.status_code != 200:
            return None
        save_name = video_id
        os.makedirs("./assets/thumbnails/youtube", exist_ok=True)
        save_path = os.path.join("./assets/thumbnails/youtube", f"{save_name}.jpg")
        print(save_path)
        print(save_name)
        with Image.open(BytesIO(rr.content)) as im:
            try:
                im.save(save_path, format="JPEG")
                return save_path
            except:
                return None


if __name__ == "__main__":
    get_yt_thumbnail("https://youtu.be/1-W6whvn8Bs?si=T7sKxZNGpHTUYKHy")
