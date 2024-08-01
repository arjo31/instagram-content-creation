import sys

sys.dont_write_bytecode = True

import requests
import streamlit as st

from src.instagram.instagram import instagram
from src.linkedin.linkedin import linkedin
from src.twitter.twitter import twitter

st.set_page_config(page_title="AI Content Creation Tool")

if "isLoggedIn" not in st.session_state:
    st.session_state.isLoggedIn = False

if "page" not in st.session_state:
    st.session_state.page = "Login"

if "user" not in st.session_state:
    st.session_state.user = ""

def signup_page():
    st.title('Sign Up')
    with st.container(border=True):
        name = st.text_input(label="Full Name", placeholder="Enter your name", key="sn")
        username = st.text_input(label="Username", placeholder="Enter your username", key="su")
        email = st.text_input(label="Email", placeholder="Enter your email", key="se")
        password = st.text_input(label="Password", placeholder="Enter your password", type="password", key="sp")
        user = {'name' : name, 'username' : username, 'email' : email, 'password' : password}
        signup_button = st.button(label="Sign Up", type="primary")
        if signup_button:
            res = requests.post(url="https://fastapi-server-fnqk.onrender.com/signup", data=user)

            if res.status_code==200:
                st.session_state.user = name
                st.session_state.isLoggedIn = True
                st.rerun()
            elif res.status_code==401:
                st.warning(res.json()['message'])
            else:
                st.error(res.json()['message'])
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("Already have an account? Log In!")
    with col2:    
        login_button = st.button(label = "Login", type="primary")
    if login_button:
        st.session_state.page = "Login"
        st.rerun()

def login_page():
    st.title(body="Login")
    with st.container(border=True):
        username = st.text_input(key="lu", label="Username", placeholder="Enter your username")
        password = st.text_input(key="lp", label="Password", placeholder="Enter your password", type='password')
        login_button = st.button(label="Log In", type="primary")
        if login_button:
            res = requests.post(url="https://fastapi-server-fnqk.onrender.com/login", data={
                'username' : username,
                'password' : password
            })
            if (res.status_code==200):
                st.session_state.user = res.json()['name']
                st.session_state.isLoggedIn = True
                st.rerun()
            elif res.status_code==401:
                st.warning(res.json()['message'])
            else:
                st.error(res.json()['message'])
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("Don't have an account? Sign Up!")
    with col2:    
        signup_button = st.button(label = "Sign Up", type="primary")
    if signup_button:
        st.session_state.page = "SignUp"
        st.rerun()        

if not st.session_state.isLoggedIn:
    if st.session_state.page == "Login":
        login_page()
    elif st.session_state.page == "SignUp":
        signup_page()
else:
    nav = st.navigation(pages=[
            st.Page(title="Instagram", page=instagram),
            st.Page(title="LinkedIn", page=linkedin),
            st.Page(title="X (formerly Twitter)", page=twitter),
        ])
    nav.run()
