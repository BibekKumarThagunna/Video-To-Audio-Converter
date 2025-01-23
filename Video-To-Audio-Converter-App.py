import os
os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "1000"  # Set max upload size to 1000 MB

import streamlit as st
import yt_dlp
from moviepy.editor import VideoFileClip

# Function to download audio from YouTube
def download_audio_from_youtube(url, output_dir="downloads"):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return f"Audio downloaded successfully! Check the {output_dir} folder."
    except Exception as e:
        return f"Error: {e}"

# Function to extract audio from a video file
def extract_audio_from_file(video_path, output_dir="downloads"):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        video = VideoFileClip(video_path)
        audio_path = os.path.join(output_dir, os.path.basename(video_path).split('.')[0] + ".mp3")
        video.audio.write_audiofile(audio_path)
        
        return f"Audio extracted successfully! Saved to {audio_path}."
    except Exception as e:
        return f"Error: {e}"

# Streamlit App
def main():
    st.title("🎵 Video to Audio Converter")
    st.write("Easily extract audio from YouTube videos or local video files.")

    # Tabs for the two functionalities
    tab1, tab2 = st.tabs(["📹 YouTube to Audio", "📂 File Upload to Audio"])

    # YouTube to Audio
    with tab1:
        st.header("YouTube to Audio")
        url = st.text_input("Enter YouTube URL:")
        if st.button("Download Audio"):
            if not url.strip():
                st.error("Please enter a valid YouTube URL.")
            else:
                with st.spinner("Downloading audio..."):
                    message = download_audio_from_youtube(url)
                    if "Error" in message:
                        st.error(message)
                    else:
                        st.success(message)

    # File Upload to Audio
    with tab2:
        st.header("File Upload to Audio")
        video_file = st.file_uploader("Upload a Video File", type=["mp4", "mkv", "avi", "mov"])
        if video_file:
            if st.button("Extract Audio"):
                # Save uploaded file to a temporary path
                temp_video_path = os.path.join("temp", video_file.name)
                os.makedirs("temp", exist_ok=True)
                with open(temp_video_path, "wb") as f:
                    f.write(video_file.read())
                
                with st.spinner("Extracting audio..."):
                    message = extract_audio_from_file(temp_video_path)
                    if "Error" in message:
                        st.error(message)
                    else:
                        st.success(message)

                # Cleanup temporary files
                os.remove(temp_video_path)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: small;'>"
        "This project was created by <b>Bibek Kumar Thagunna</b>."
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
