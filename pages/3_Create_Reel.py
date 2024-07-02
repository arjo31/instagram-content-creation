import requests
import streamlit as st

st.title("Create a Reel")

st.session_state.page = "Reel Creation"

st.sidebar.success(f"You are currently in {st.session_state.page} Page")

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

def transcript_video(video):
    file = {'file' : video}
    data = {'id' : video.file_id, 'name' : video.name}
    res = requests.post(url="http://localhost:5000/transcript-video", files=file, data=data)
    return res

def create_reel_caption(video, text):
    file = {'file' : video}
    data = {'data' : text}
    res = requests.post(url="http://localhost:5000/create-caption-from-video", files = file, data = data)
    return res

video_file = st.file_uploader(
    label="Upload your reel",
    accept_multiple_files=False,
    type=['mp4', 'mov', 'mkv', 'avi', 'wmv']
)

if video_file and video_file != st.session_state.uploaded_file:
    st.session_state.uploaded_file = video_file
    st.success("File uploaded successfully")

content = st.text_input(label="Enter your thoughts for the reel's caption", placeholder="Additional thoughts for the reel")
    
button = st.button("Upload Video", type='primary')

if button:
    with st.spinner("Generating Caption..."):
        # res = transcript_video(video=video_file)
        # if (res.status_code==501):
        #     st.error(res.json()['message'])
        # transciption = res.json()['message']
        res = create_reel_caption(video=video_file, text=content)
        if (res.status_code==501):
            st.error(res.json()['message'])
        else : st.write(res.json()['message'])