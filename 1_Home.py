import requests
import streamlit as st

st.set_page_config(page_title="Instagram AI Tool")

st.title("Instagram AI Creation Tool")

st.markdown("This AI Tool by Spillmate aims to revolutionize content creation for Instagram by using cutting edge AI tools and models and leveraging the power of LLMs by using the Google Gemini Pro API to answer all your queries.")


if "page" not in st.session_state:
    st.session_state.page = ""

st.session_state.page = "Home"

st.sidebar.success(f"You are currently in {st.session_state.page} Page")

