import streamlit as st
import requests

st.title("Reply to a post")

st.session_state.page = "Reply"

st.sidebar.success(f"You are currently in {st.session_state.page} Page")

comment = st.text_input(label="Enter the comment you want to reply to", placeholder="Comment",max_chars=10000)

reply = st.button("Generate Reply", type='primary')

def generate_reply(comment : str):
    data = {'comment' : comment}
    response = requests.post(url="http://localhost:5000/generate-reply", data = data)
    return response

if (reply and len(comment)!=0):
    res = generate_reply(comment=comment)
    if (res.status_code==200):
        st.write(res.json()['message'])
    else : st.error(res.json()['message'])