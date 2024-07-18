import requests
import streamlit as st


def twitter():
    st.title("Spillmate Twitter Content Generation")

    def generate_required_content(prompt : str):
        url = "http://localhost:5000/generate-twitter-content"
        data = {'prompt' : prompt}
        res = requests.post(url=url, data=data)
        return res

    st.session_state.page = "Twitter"

    st.sidebar.success(f"Welcome {st.session_state.user}! You are currently in {st.session_state.page} Page")
    
    feature = st.selectbox("What's your idea?", ["Create a post...", "Write a reply..."])

    user_input = st.text_area("Type your content creation idea")

    if st.button("Generate Content"):
        if feature == "Create a post...":
            final_response = generate_required_content(f"Write a Twitter post about {user_input}")
        elif feature == "Write a reply...":
            final_response = generate_required_content(f"Write an appropriate reply to this Twitter post: {user_input}")
        
        if (final_response.status_code==200):
            st.write(final_response.json()['message'])
        else: st.error(final_response.json()['message'])
