import streamlit as st
import subprocess
import os
import tempfile

from thumbnail import get_ytmusic_thumbnail


def generate_output_video(bg_image_path: str) -> str:
    """Generates the final video using a bash script that uses ffmpeg

    Args:
        background_temp_file_path (str): path to the background image

    Returns:
        str: path to the output video
    """
    result = subprocess.run(
        ["scripts/generateVideo.sh", bg_image_path], capture_output=True
    )
    output_video_path = str(result.stdout).lstrip("b'").rstrip("\\n'")
    return output_video_path


def display_generated_video(output_video_path):
    st.write(f"Generated video saved to {output_video_path}")
    st.video(output_video_path, loop=False, autoplay=True, muted=False)
    # Display a slider to adjust video size
    # DEFAULT_WIDTH = 80
    # width = st.sidebar.slider(
    #     label="Width", min_value=0, max_value=100, value=DEFAULT_WIDTH, format="%d%%"
    # )

    # width = max(width, 0.01)
    # side = max((100 - width) / 2, 0.01)

    # _, container, _ = st.columns([side, width, side])
    # container.video(output_video_path, loop=False, autoplay=True, muted=False)


st.set_page_config(
    page_title="Paul Allen", page_icon=":speaking_head_in_silhouette:", layout="centered"
)

st.subheader("Upload your own cover art!")
uploaded_background = st.file_uploader(
    "Upload image",
    type=["png", "jpg", "jpeg", "webp"],
    help="Upload the image that would be the backgroung of ouput video",
)

st.divider()
st.subheader("OR")
st.divider()

st.subheader("Paste the YouTube Music link of your favourite song!")
song_url = st.text_input(
    ("YouTube Music URL"), value=None
)
if song_url is not None:
    bg_image_path = get_ytmusic_thumbnail(song_url)
    output_video_path = generate_output_video(bg_image_path)
    display_generated_video(output_video_path)


if uploaded_background is not None:
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as cover_art_directory:
        # Save the uploaded file to the temporary directory
        background_temp_file_path = os.path.join(
            cover_art_directory, uploaded_background.name
        )
        with open(background_temp_file_path, "wb") as temp_file:
            temp_file.write(uploaded_background.read())

        st.write(f"File saved to {background_temp_file_path}")

        output_video_path = generate_output_video(background_temp_file_path)
        display_generated_video(output_video_path)
