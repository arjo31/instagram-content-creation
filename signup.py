import streamlit as st
import os

from dotenv import load_dotenv

load_dotenv()

st.title(body="Signup")
with st.container(border=True):
    username = st.text_input(label="Username", placeholder="Enter your username")
    name = st.text_input(label="Name", placeholder="Enter your Full Name")
    email = st.text_input(label="Email", placeholder="Enter your email")
    password = st.text_input(label="Password", placeholder="Enter your password", type='password')

    signup_button = st.button(label="Sign Up", type="primary")