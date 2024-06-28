import streamlit as st

st.title("Create a Post")

st.session_state.page = "Post Creation"

st.sidebar.success(f"You are currently in {st.session_state.page} Page")