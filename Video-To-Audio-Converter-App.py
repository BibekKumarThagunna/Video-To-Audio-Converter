import streamlit as st
import os
import yt_dlp
from moviepy.editor import VideoFileClip
import tempfile

# Function to download audio from YouTube and return bytes
def download_audio_from_youtube(url):
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # Find the generated mp3 file
                mp3_files = [f for f in os.listdir(tmp_dir) if f.endswith('.mp3')]
                if not mp3_files:
                    return None, "No audio file found"
                
                mp3_path = os.path.join(tmp_dir, mp3_files[0])
                with open(mp3_path, 'rb') as f:
                    audio_bytes = f.read()
                
                return audio_bytes, mp3_files[0]
    except Exception as e:
        return None, f"Error: {str(e)}"

# Function to extract audio from file and return bytes
def extract_audio_from_file(video_path):
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Generate output filename
            base_name = os.path.basename(video_path).split('.')[0]
            output_path = os.path.join(tmp_dir, f"{base_name}.mp3")
            
            # Process video
            with VideoFileClip(video_path) as video:
                video.audio.write_audiofile(output_path)
            
            # Read generated audio file
            with open(output_path, 'rb') as f:
                audio_bytes = f.read()
            
            return audio_bytes, f"{base_name}.mp3"
    except Exception as e:
        return None, f"Error: {str(e)}"

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
        if st.button("Prepare YouTube Audio"):
            if not url.strip():
                st.error("Please enter a valid YouTube URL.")
            else:
                with st.spinner("Processing audio..."):
                    audio_bytes, filename = download_audio_from_youtube(url)
                    
                    if audio_bytes:
                        file_size = len(audio_bytes) / (1024 * 1024)  # Convert to MB
                        st.success(f"Audio ready! File size: {file_size:.2f} MB")
                        
                        # Add download button
                        st.download_button(
                            label="💾 Download Audio",
                            data=audio_bytes,
                            file_name=filename,
                            mime="audio/mpeg"
                        )
                    else:
                        st.error(filename)

    # File Upload to Audio
    with tab2:
        st.header("File Upload to Audio")
        video_file = st.file_uploader("Upload a Video File", type=["mp4", "mkv", "avi", "mov"])
        if video_file and st.button("Prepare File Audio"):
            with st.spinner("Extracting audio..."):
                # Save uploaded file to temporary location
                with tempfile.TemporaryDirectory() as tmp_dir:
                    temp_path = os.path.join(tmp_dir, video_file.name)
                    with open(temp_path, "wb") as f:
                        f.write(video_file.getbuffer())
                    
                    # Process audio
                    audio_bytes, filename = extract_audio_from_file(temp_path)
                    
                    if audio_bytes:
                        file_size = len(audio_bytes) / (1024 * 1024)  # Convert to MB
                        st.success(f"Audio ready! File size: {file_size:.2f} MB")
                        
                        # Add download button
                        st.download_button(
                            label="💾 Download Audio",
                            data=audio_bytes,
                            file_name=filename,
                            mime="audio/mpeg"
                        )
                    else:
                        st.error(filename)

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: small;'>"
        "This project is created by <b>Bibek Kumar Thagunna</b>."
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
