import streamlit as st

st.title("Instagram AI Creation Tool")

st.markdown("This AI Tool by Spillmate aims to revolutionize content creation for Instagram by using cutting edge AI tools and models and leveraging the power of LLMs by using the Google Gemini Pro API to answer all your queries.")

st.session_state.page = "Home"

st.sidebar.success(f"You are currently in {st.session_state.page} Page")

