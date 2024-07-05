# store generated video path in session_state and avoid re-rendering
import streamlit as st
import subprocess
import os
import tempfile
import re
from datetime import datetime, timedelta

from ytmusic_thumbnail import get_ytmusic_thumbnail
from youtube_thumbnail import get_yt_thumbnail
from spotify_thumbnail import get_spotify_thumbnail

if "video_state" not in st.session_state:
    st.session_state["video_state"] = (
        []
    )  # list of dicts. key:bg_image_path :: value: ouput_video_path

if "song_state" not in st.session_state:
    st.session_state["song_state"] = []  # list of dicts. key:url :: value: song_path


def generate_output_video_user_upload(bg_image_path: str) -> str:
    """Generates the final video using a bash script that uses ffmpeg

    Args:
        background_temp_file_path (str): path to the background image

    Returns:
        str: path to the output video
    """
    for dictionary in st.session_state["video_state"]:
        if dictionary.get(bg_image_path, None) is not None:
            print("using already generated video")
            return dictionary[bg_image_path]
        else:
            continue
    result = subprocess.run(
        ["scripts/generateVideoUserUpload.sh", bg_image_path], capture_output=True
    )
    output_video_path = str(result.stdout).lstrip("b'").rstrip("\\n'")
    st.session_state["video_state"].append({bg_image_path: output_video_path})

    return output_video_path


def generate_output_video_spotify(bg_image_path: str) -> str:
    """Generates the final video using a bash script that uses ffmpeg

    Args:
        background_temp_file_path (str): path to the background image

    Returns:
        str: path to the output video
    """
    for dictionary in st.session_state["video_state"]:
        if dictionary.get(bg_image_path, None) is not None:
            print("using already generated video")
            return dictionary[bg_image_path]
        else:
            continue
    result = subprocess.run(
        ["scripts/generateVideoSpotify.sh", bg_image_path], capture_output=True
    )
    output_video_path = str(result.stdout).lstrip("b'").rstrip("\\n'")
    st.session_state["video_state"].append({bg_image_path: output_video_path})

    return output_video_path


def generate_output_video_ytmusic(bg_image_path: str) -> str:
    """Generates the final video using a bash script that uses ffmpeg

    Args:
        background_temp_file_path (str): path to the background image

    Returns:
        str: path to the output video
    """
    for dictionary in st.session_state["video_state"]:
        if dictionary.get(bg_image_path, None) is not None:
            print("using already generated video")
            return dictionary[bg_image_path]
        else:
            continue
    result = subprocess.run(
        ["scripts/generateVideoYTMusic.sh", bg_image_path], capture_output=True
    )
    output_video_path = str(result.stdout).lstrip("b'").rstrip("\\n'")
    st.session_state["video_state"].append({bg_image_path: output_video_path})

    return output_video_path


def generate_output_video_youtube(bg_image_path: str) -> str:
    """Generates the final video using a bash script that uses ffmpeg. It uses a landscape bateman video

    Args:
        background_temp_file_path (str): path to the background image

    Returns:
        str: path to the output video
    """
    # session state looks like this
    # {'output_video_path': [{'./assets/thumbnails/youtube/1-W6whvn8Bs.jpg': './outputs/out_14-55-14.mp4'}]}
    for dictionary in st.session_state["video_state"]:
        if dictionary.get(bg_image_path, None) is not None:
            print("using already generated thumbnail")
            return dictionary[bg_image_path]
        else:
            continue
    result = subprocess.run(
        ["scripts/generateVideoYouTube.sh", bg_image_path], capture_output=True
    )
    output_video_path = str(result.stdout).lstrip("b'").rstrip("\\n'")
    st.session_state["video_state"].append({bg_image_path: output_video_path})
    print(st.session_state)
    return output_video_path


def download_song_spotify(url: str) -> str:
    # if the song is already downloaded, no need to download again.
    for dictionary in st.session_state["song_state"]:
        if dictionary.get(url, None) is not None:
            print("using already downloaded song: spotify")
            return dictionary[url]
        else:
            continue
    # spotify_dl downloads the song, and outputs a lot of things on stdout, among them is save location
    result = subprocess.run(
        ["spotify_dl", "-l", url, "-o", "./audio"], capture_output=True
    )
    pattern = r"\[download\] Destination: (.+?)\n|\[download\] (.+?) has already been downloaded\n"
    match = re.search(pattern, result.stdout.decode("utf-8"))
    if match:
        # Check which group matched and return the appropriate one
        song_path = match.group(1) if match.group(1) else match.group(2)
        return song_path


def get_song_duration(song_path: str) -> float:
    result = subprocess.run(
        ['ffprobe', '-i', song_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
        )
    duration_in_seconds = result.stdout.strip()
    return float(duration_in_seconds)


def display_downloaded_song(song_path):
    st.audio(song_path, format="audio/webm", autoplay=False)


def display_generated_video(output_video_path):
    st.video(output_video_path, loop=False, autoplay=True, muted=False)


st.set_page_config(
    page_title="Paul Allen",
    page_icon=":speaking_head_in_silhouette:",
    layout="centered",
)

st.subheader("Upload your own cover art!", divider="rainbow")
uploaded_background = st.file_uploader(
    "Upload image",
    type=["png", "jpg", "jpeg", "webp"],
    help="Upload the image that would be the backgroung of ouput video",
)
if uploaded_background is not None:
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as cover_art_directory:
        # Save the uploaded file to the temporary directory
        background_temp_file_path = os.path.join(
            cover_art_directory, uploaded_background.name
        )
        with open(background_temp_file_path, "wb") as temp_file:
            temp_file.write(uploaded_background.read())

        # st.write(f"File saved to {background_temp_file_path}")

        output_video_path = generate_output_video_user_upload(background_temp_file_path)
        display_generated_video(output_video_path)

st.subheader("OR")

st.subheader("Paste the Spotify link of your favourite song!", divider="rainbow")
spotify_url = st.text_input(("Spotify URL"), value=None)
if spotify_url is not None:
    bg_image_path = get_spotify_thumbnail(spotify_url)
    # output_video_path = generate_output_video_spotify(bg_image_path)
    # display_generated_video(output_video_path)

    song_path = download_song_spotify(spotify_url)
    song_duration_in_seconds = get_song_duration(song_path)

    delta = timedelta(seconds=song_duration_in_seconds)
    min_datetime = datetime(1970, 1, 1)
    max_datetime = min_datetime + delta

    start_time_slider = st.slider(
        "Start Time",
        min_value=min_datetime,
        max_value=max_datetime,
        step=timedelta(1),
        format="mm:ss",
        help="From this start time, the song will be added to the generated video",
    )
    display_downloaded_song(song_path)


st.subheader("Paste the YTMusic link of your favourite song!", divider="rainbow")
st.info("You can even paste the link of your YTMusic playlist or album", icon="🔥")
ytmusic_url = st.text_input(("YouTube Music URL"), value=None)
if ytmusic_url is not None:
    bg_image_path = get_ytmusic_thumbnail(ytmusic_url)
    output_video_path = generate_output_video_ytmusic(bg_image_path)
    display_generated_video(output_video_path)


st.subheader("Paste the YouTube link of your favourite song!", divider="rainbow")
youtube_url = st.text_input(("YouTube URL"), value=None)
if youtube_url is not None:
    bg_image_path = get_yt_thumbnail(youtube_url)
    output_video_path = generate_output_video_youtube(bg_image_path)
    display_generated_video(output_video_path)
