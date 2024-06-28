import requests
import streamlit as st

st.title("Create a Reel")

st.session_state.page = "Reel Creation"

st.sidebar.success(f"You are currently in {st.session_state.page} Page")

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

def send_video(video):
    file = {'file' : video}
    data = {'id' : video.file_id, 'name' : video.name}
    res = requests.post(url="http://localhost:5000/upload-video", files=file, data=data)
    return res

video_file = st.file_uploader(
    label="Upload your reel",
    accept_multiple_files=False,
    type=['mp4', 'mov', 'mkv', 'avi', 'wmv']
)

if video_file and video_file != st.session_state.uploaded_file:
    st.session_state.uploaded_file = video_file
    st.success("File uploaded successfully")
    
button = st.button("Upload Video", type='primary')

if button:
    with st.spinner("Generating Transcription"):
        res = send_video(video=video_file)
        st.write(res.json()['message'])
