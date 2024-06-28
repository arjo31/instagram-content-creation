import streamlit as st

st.title("Reply to a post")

st.session_state.page = "Reply"

st.sidebar.success(f"You are currently in {st.session_state.page} Page")