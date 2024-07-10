import requests
import streamlit as st

st.title("Create a Caption for a Reel")

st.session_state.page = "Reel Creation"
st.sidebar.success(f"You are currently in {st.session_state.page} Page")

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

if 'isContent' not in st.session_state:
    st.session_state.isContent = False

if 'isYesButton' not in st.session_state:
    st.session_state.isYesButton = None

def create_reel_caption(video, text):
    file = {'file': video}
    data = {'data': text}
    res = requests.post(url="http://localhost:5000/create-caption-from-video", files=file, data=data)
    return res

try:
    video_file = st.file_uploader(
        label="Upload your reel",
        accept_multiple_files=False,
        type=['mp4', 'mov', 'mkv', 'avi', 'wmv']
    )

    if video_file and video_file != st.session_state.uploaded_file:
        try:
            st.session_state.uploaded_file = video_file
            st.toast(body="File Successfully Uploaded! :white_check_mark:")
            st.session_state.isContent = False
            st.session_state.isYesButton = None

        except Exception as e:
            st.toast(body="Invalid video file! Please upload a valid video file :heavy_exclamation_mark:")
            st.warning(str(e))
            st.session_state.uploaded_file = None
except Exception as e:
    st.toast(body="File Not Uploaded :heavy_exclamation_mark:")
    st.warning(str(e))

st.markdown("Do you want to add extra thoughts for your reel caption?")

col1, col2, col3, col4, col5 = st.columns(5)

with col2:
    yes = st.button("Yes", key="yes", use_container_width=True)

with col4:
    no = st.button("No", key="no", use_container_width=True)

if yes and st.session_state.uploaded_file:
    st.session_state.isYesButton = True
    st.session_state.isContent = True
elif no and st.session_state.uploaded_file:
    st.session_state.isYesButton = False
    st.session_state.isContent = True

if st.session_state.isContent:
    if st.session_state.uploaded_file:
        if st.session_state.isYesButton:
            try:
                content = st.text_input(label="Enter your thoughts for the reel's caption", placeholder="Additional thoughts for the reel")
                button = st.button("Upload Video", key="upload_button_yes", type="primary")
                if button:
                    with st.spinner("Generating Caption..."):
                        st.session_state.uploaded_file.seek(0)
                        res = create_reel_caption(video=st.session_state.uploaded_file, text=content)
                        if res.status_code == 200:
                            st.write(res.json()['message'])
                        else:
                            st.error(res.json()['message'])
            except Exception as e:
                st.toast(body="An error occurred during caption generation :heavy_exclamation_mark:")
                st.warning(str(e))
        else:
            try:
                button = st.button("Upload Video", key="upload_button_no", type="primary")
                if button:
                    with st.spinner("Generating Caption..."):
                        st.session_state.uploaded_file.seek(0)
                        res = create_reel_caption(video=st.session_state.uploaded_file, text="No extra thoughts")
                        if res.status_code == 200:
                            st.write(res.json()['message'])
                        else:
                            st.error(res.json()['message'])
            except Exception as e:
                st.toast(body="An error occurred during caption generation :heavy_exclamation_mark:")
                st.warning(str(e))
    else:
        st.toast(body="No video file uploaded! Please upload a video file first :heavy_exclamation_mark:")
