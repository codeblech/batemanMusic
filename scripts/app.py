import streamlit as st
import subprocess
import os
import tempfile

st.write("I have to return some videotapes")
uploaded_background = st.file_uploader(
    "Upload your own cover art!",
    type=["png", "jpg", "jpeg", "webp"],
    help="Upload the image that would be the backgroung of ouput video",
)

if uploaded_background is not None:
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as cover_art_directory:
        # Save the uploaded file to the temporary directory
        background_temp_file_path = os.path.join(cover_art_directory, uploaded_background.name)
        with open(background_temp_file_path, "wb") as temp_file:
            temp_file.write(uploaded_background.read())

        st.write(f"File saved to {background_temp_file_path}")
        result = subprocess.run(["scripts/generateVideo.sh", background_temp_file_path], capture_output=True)
        output_video_path = str(result.stdout).lstrip("b'").rstrip("\\n'")
        st.write(output_video_path)
        st.write(f"Generated video saved to {output_video_path}")
        st.video(output_video_path, loop=False, autoplay=True, muted=False)


