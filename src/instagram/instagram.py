import sys

sys.dont_write_bytecode = True

import requests
import streamlit as st


def send_response(content):
    data = {'user_input' : content}
    res = requests.post(url="http://localhost:5000/create-post", data=data)
    return res

def create_reel_caption(video, text):
    file = {'file': video}
    data = {'data': text}
    res = requests.post(url="http://localhost:5000/create-caption-from-video", files=file, data=data)
    return res

def generate_reply(comment : str):
    data = {'comment' : comment}
    response = requests.post(url="http://localhost:5000/generate-reply", data = data)
    return response

def instagram():
    st.title("Spillmate Instagram Content Generation")

    if st.session_state.page=="Login":
        st.toast(body="Login Successful:white_check_mark:")
    elif st.session_state.page=="SignUp":
        st.toast(body="Registration Successful:white_check_mark:")

    st.session_state.page = "Instagram"

    st.sidebar.success(f"Welcome {st.session_state.user}! You are currently in {st.session_state.page} Page")

    options = st.selectbox(label="Select a tool you want to use", options=["Select an option","Create a Post", "Create a caption for a reel", "Reply to a comment"])

    if options=="Create a Post":
        col1, col2 = st.columns([4, 1])
        with col1:
            st.title("Create a Post")

        if "messages" not in st.session_state:
            st.session_state.messages = [{'role' : 'ai', 'content' : 'Hello! How may I help you with your content creation?'}]

        st.markdown(
            """
            <style>
            .centered-button {
                display: flex;
                align-items: center;
                justify-content: center;
                position: absolute;
                height: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        with col2:
            with st.container():
                st.write('<div class="centered-button">', unsafe_allow_html=True)
                if st.button('Clear Chat', type='primary'):
                    st.session_state.messages = [{'role':'ai', 'content':'Hello! How may I help you with your content creation?'}]
                st.write('</div>', unsafe_allow_html=True)

        def add_message(role, content):
            st.session_state.messages.append({'role' : role, 'content' : content})

        for message in st.session_state.messages:
            if (st.session_state.messages[-1]['role']=="user"):
                st.session_state.messages.pop()
            with st.chat_message(message['role']):
                    st.write(message['content'])

        if user_input:=st.chat_input("Provide your post idea!"):
            add_message('user', user_input)
            with st.chat_message('user'):
                st.write(user_input)
            response = send_response(user_input)
            if (response.status_code==200):
                response = response.json()['message']
                add_message('ai', response)
                with st.chat_message('ai'):
                    st.write(response)
            else: st.error(response.json()['message'])

    elif options=="Create a caption for a reel":
        st.title("Create a Caption for a Reel")
        if 'uploaded_file' not in st.session_state:
            st.session_state.uploaded_file = None

        if 'isContent' not in st.session_state:
            st.session_state.isContent = False

        if 'isYesButton' not in st.session_state:
            st.session_state.isYesButton = None

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

    elif options=="Reply to a comment":
        st.title("Reply to a post")

        comment = st.text_input(label="Enter the comment you want to reply to", placeholder="Comment",max_chars=10000)

        reply = st.button("Generate Reply", type='primary')

        if (reply and len(comment)!=0):
            res = generate_reply(comment=comment)
            if (res.status_code==200):
                st.write(res.json()['message'])
            else : st.error(res.json()['message'])