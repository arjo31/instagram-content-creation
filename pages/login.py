import streamlit as st

st.set_page_config(page_title="Instagram AI Tool")

if "isLoggedIn" not in st.session_state:
    st.session_state.isLoggedIn = False

if "page" not in st.session_state:
    st.session_state.page = "Login"

if (st.session_state.page=="Login" and st.session_state.isLoggedIn==False):
    st.title(body="Login")
    with st.container(border=True):
        username = st.text_input(label="Username", placeholder="Enter your username")
        password = st.text_input(label="Password", placeholder="Enter your password", type='password')

        login_button = st.button(label="Log In", type="primary")
        if login_button:
            st.session_state.page = "Home"
            st.session_state.isLoggedIn = True
            st.rerun()
else:
    nav = st.navigation(pages=[
        st.Page(title="Home", page="Home.py"),
        st.Page(title="Create Post", page="Create_Post.py"),
        st.Page(title="Create Reel Caption", page="Create_Reel.py"),
        st.Page(title="Reply to a Comment", page="Reply.py")
    ])
    nav.run()