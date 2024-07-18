import sys

sys.dont_write_bytecode = True

import requests
import streamlit as st


def linkedin():
    def generate_linkedin_posts(prompt : str, max_length : int):
        url = "http://localhost:5000/generate-linkedin-content"
        data = {'prompt' : prompt, 'max_length' : max_length}
        res = requests.post(url=url, data=data)
        return res
    
    st.session_state.page = "LinkedIn"

    st.sidebar.success(f"Welcome {st.session_state.user}! You are currently in {st.session_state.page} Page")

    st.title("Spillmate LinkedIn Content Generation")

    feature = st.selectbox("Select a feature", 
                            ["Write Post", "Write Article Summary", "Write Comment Reply", 
                            "Generate Hashtags", "Optimize Content", "Create Poll"])

    user_input = st.text_area("Enter your prompt:")

    min_length = st.number_input("Minimum character count:", min_value=100, max_value=2000, value=1300)
    max_length = st.number_input("Maximum character count:", min_value=100, max_value=3000, value=2000)

    if st.button("Generate"):
        if feature == "Write Post":
            response = generate_linkedin_posts(f"Write a LinkedIn post about: {user_input}", max_length)
        elif feature == "Write Article Summary":
            response = generate_linkedin_posts(f"Write a summary for a LinkedIn article about: {user_input}", max_length)
        elif feature == "Write Comment Reply":
            response = generate_linkedin_posts(f"Write a professional reply to this LinkedIn comment: {user_input}", max_length)
        elif feature == "Generate Hashtags":
            response = generate_linkedin_posts(f"Generate 3-5 relevant LinkedIn hashtags for: {user_input}", max_length)
        elif feature == "Optimize Content":
            response = generate_linkedin_posts(f"Analyze and optimize this LinkedIn content: {user_input}", max_length)
        elif feature == "Create Poll":
            response = generate_linkedin_posts(f"Create a LinkedIn poll about: {user_input}", max_length)
        
        if response.status_code==200:
            msg = response.json()['message']
            st.write(msg)
            char_count = len(msg)
            st.write(f"Character count: {char_count}")
            if char_count < min_length:
                st.warning(f"Post is shorter than the specified minimum of {min_length} characters.")
            elif char_count > max_length:
                st.warning(f"Post is longer than the specified maximum of {max_length} characters.")
        else:
            st.error(response.json()['message'])