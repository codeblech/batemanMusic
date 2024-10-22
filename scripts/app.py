import streamlit as st
import subprocess
import os
import tempfile
import re
from datetime import datetime, timedelta
import mimetypes

import yt_dlp

from ytmusic_thumbnail import get_ytmusic_thumbnail
from youtube_thumbnail import get_yt_thumbnail
from spotify_thumbnail import get_spotify_thumbnail

if "video_state" not in st.session_state:
    st.session_state["video_state"] = {}

if "song_state" not in st.session_state:
    st.session_state["song_state"] = {}


def generate_output_video_user_upload(bg_image_path: str) -> str:
    """Generates the final video using a bash script that uses ffmpeg

    Args:
        background_temp_file_path (str): path to the background image

    Returns:
        str: path to the output video
    """
    if bg_image_path in st.session_state["video_state"]:
        print("Using already generated video")
        return st.session_state["video_state"][bg_image_path]

    result = subprocess.run(
        ["scripts/generateVideoUserUpload.sh", bg_image_path], capture_output=True
    )
    output_video_path = str(result.stdout).lstrip("b'").rstrip("\\n'")
    st.session_state["video_state"][bg_image_path] = output_video_path

    return output_video_path


def generate_output_video_spotify(bg_image_path: str) -> str:
    """Generates the final video using a bash script that uses ffmpeg

    Args:
        background_temp_file_path (str): path to the background image

    Returns:
        str: path to the output video
    """
    if bg_image_path in st.session_state["video_state"]:
        print("Using already generated video")
        return st.session_state["video_state"][bg_image_path]

    result = subprocess.run(
        ["scripts/generateVideoSpotify.sh", bg_image_path], capture_output=True
    )
    output_video_path = str(result.stdout).lstrip("b'").rstrip("\\n'")
    st.session_state["video_state"][bg_image_path] = output_video_path

    return output_video_path


def generate_output_video_ytmusic(bg_image_path: str) -> str:
    """Generates the final video using a bash script that uses ffmpeg

    Args:
        background_temp_file_path (str): path to the background image

    Returns:
        str: path to the output video
    """
    if bg_image_path in st.session_state["video_state"]:
        print("Using already generated video")
        return st.session_state["video_state"][bg_image_path]

    result = subprocess.run(
        ["scripts/generateVideoYTMusic.sh", bg_image_path], capture_output=True
    )
    output_video_path = str(result.stdout).lstrip("b'").rstrip("\\n'")
    st.session_state["video_state"][bg_image_path] = output_video_path

    return output_video_path


def generate_output_video_youtube(bg_image_path: str) -> str:
    """Generates the final video using a bash script that uses ffmpeg. It uses a landscape bateman video

    Args:
        background_temp_file_path (str): path to the background image

    Returns:
        str: path to the output video
    """
    if bg_image_path in st.session_state["video_state"]:
        print("Using already generated thumbnail")
        return st.session_state["video_state"][bg_image_path]

    result = subprocess.run(
        ["scripts/generateVideoYouTube.sh", bg_image_path], capture_output=True
    )
    output_video_path = str(result.stdout).lstrip("b'").rstrip("\\n'")
    st.session_state["video_state"][bg_image_path] = output_video_path

    return output_video_path


def download_song_spotify(url: str) -> str:
    """downloads song using spotify_dl

    Args:
        url (str): url to track on spotify

    Returns:
        str: path of the downloaded song
    """
    # if the song is already downloaded, no need to download again.
    if url in st.session_state["song_state"]:
        print("Using already downloaded song: spotify")
        return st.session_state["song_state"][url]

    # spotify_dl downloads the song, and outputs a lot of things on stdout, among them is save location
    os.makedirs("./audio/spotify", exist_ok=True)
    result = subprocess.run(
        ["spotify_dl", "-l", url, "-o", "./audio/spotify", "-m"], capture_output=True
    )
    pattern = r"\[download\] Destination: (.+?)\n|\[download\] (.+?) has already been downloaded\n"
    match = re.search(pattern, result.stdout.decode("utf-8"))
    if match:
        song_path = match.group(1) if match.group(1) else match.group(2)
        st.session_state["song_state"][url] = song_path
        print(song_path)
        return song_path


def download_song_youtube(url: str) -> str:
    """downloads video using yt_dlp and extracts audio from it.

    Args:
        url (str): url to song on youtube

    Returns:
        str: path of the downloaded song
    """
    # if the song is already downloaded, no need to download again.
    if url in st.session_state["song_state"]:
        print("Using already downloaded song: youtube")
        return st.session_state["song_state"][url]

    output_location = {}

    def hook(d):
        if d["status"] == "finished":
            output_location["filename"] = d["filename"]

    os.makedirs("./audio/youtube", exist_ok=True)
    urls = [url]

    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "aac",
            }
        ],
        "outtmpl": os.path.join(
            "./audio/youtube", "%(title)s.%(ext)s"
        ),  # Set the output directory and filename template
        "progress_hooks": [hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(urls)
        print("youtube-dl error code: ", error_code)
    return output_location.get("filename", "Download failed or file not found")


def get_song_duration(song_path: str) -> float:
    """finds the duration of a song in seconds

    Args:
        song_path (str): path to song

    Returns:
        float: song duration in seconds
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-i",
            song_path,
            "-show_entries",
            "format=duration",
            "-v",
            "quiet",
            "-of",
            "csv=p=0",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    duration_in_seconds = result.stdout.strip()
    print("duration: ", duration_in_seconds)
    return float(duration_in_seconds)


def combine_audio_video(
    ouput_video_path: str, song_path: str, delay_in_seconds: int
) -> str:
    """combines the given audio and video with delay added from start of the audio.

    Args:
        ouput_video_path (str): path to the video
        song_path (str): path to the audio
        delay_in_seconds (int): a delay of 69 makes the audio start from the 01:09 mm:ss mark

    Returns:
        str: _description_
    """
    result = subprocess.run(
        [
            "./scripts/combineAudioVideo.sh",
            song_path,
            output_video_path,
            str(delay_in_seconds),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    final_video_path = result.stdout.strip()
    print("final_path: ", final_video_path)
    return final_video_path


def display_downloaded_song_spotify(song_path):
    st.audio(song_path, format="audio/webm", autoplay=False)


def display_downloaded_song_youtube(song_path):
    try:
        st.audio(song_path, format="audio/m4a", autoplay=False)
    except:
        mime_type, _ = mimetypes.guess_type(song_path)
        st.audio(song_path, format=mime_type)


def display_generated_video(output_video_path):
    st.video(output_video_path, loop=False, autoplay=True, muted=False)


st.set_page_config(
    page_title="Paul Allen",
    page_icon=":speaking_head_in_silhouette:",
    layout="centered",
)
st.info("Functionality to add music is in beta, and not available for YTMusic and uploaded images")
st.subheader("Upload your own cover art!", divider="rainbow")
uploaded_background = st.file_uploader(
    "Upload image",
    type=["png", "jpg", "jpeg", "webp"],
    help="Upload the image that would be the background of the output video",
)
if uploaded_background is not None:
    with tempfile.TemporaryDirectory() as cover_art_directory:
        background_temp_file_path = os.path.join(
            cover_art_directory, uploaded_background.name
        )
        with open(background_temp_file_path, "wb") as temp_file:
            temp_file.write(uploaded_background.read())

        output_video_path = generate_output_video_user_upload(background_temp_file_path)
        display_generated_video(output_video_path)

st.subheader("OR")

st.subheader("Paste the Spotify link of your favourite song!", divider="rainbow")
spotify_url = st.text_input(("Spotify URL"), value=None)
if spotify_url is not None:
    bg_image_path = get_spotify_thumbnail(spotify_url)
    output_video_path = generate_output_video_spotify(bg_image_path)
    display_generated_video(output_video_path)

    song_path = download_song_spotify(spotify_url)
    display_downloaded_song_spotify(song_path)
    song_duration_in_seconds = get_song_duration(song_path)

    min_datetime = datetime(1970, 1, 1)
    max_datetime = min_datetime + timedelta(seconds=song_duration_in_seconds)

    start_time = st.slider(
        "Start Time",
        min_value=min_datetime,
        max_value=max_datetime,
        step=timedelta(seconds=1),
        format="mm:ss",
        help="From this start time, the song will be added to the generated video",
    )
    delay_in_seconds = start_time.minute * 60 + start_time.second
    st.write(
        f"Click the 'Embed Audio' button to add audio to the video, starting from {start_time.minute}:{start_time.second}"
    )
    if st.button(label="Embed Audio 🎧"):
        final_video_path = combine_audio_video(
            output_video_path, song_path, delay_in_seconds
        )
        display_generated_video(final_video_path)


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

    song_path = download_song_youtube(youtube_url)
    display_downloaded_song_youtube(song_path)
    song_duration_in_seconds = get_song_duration(song_path)

    min_datetime = datetime(1970, 1, 1)
    max_datetime = min_datetime + timedelta(seconds=song_duration_in_seconds)

    start_time = st.slider(
        "Start Time",
        min_value=min_datetime,
        max_value=max_datetime,
        step=timedelta(seconds=1),
        format="mm:ss",
        help="From this start time, the song will be added to the generated video",
    )
    delay_in_seconds = start_time.minute * 60 + start_time.second
    st.write(
        f"Click the 'Embed Audio' button to add audio to the video, starting from {start_time.minute}:{start_time.second}"
    )
    if st.button(label="Embed Audio 🎧"):
        final_video_path = combine_audio_video(
            output_video_path, song_path, delay_in_seconds
        )
        display_generated_video(final_video_path)
