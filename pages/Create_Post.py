import requests
import streamlit as st

st.session_state.page = "Post Creation"

st.sidebar.success(f"You are currently in {st.session_state.page} Page")

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

def send_response(content):
    data = {'user_input' : content}
    res = requests.post(url="http://localhost:5000/create-post", data=data)
    return res

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