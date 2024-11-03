# https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app

from dotenv import load_dotenv
import streamlit as st
import os
import uuid
from pages import home, edit_image
import config


# init sessions
if 'initial_sidebar_state' not in st.session_state:
    st.session_state.initial_sidebar_state = "collapsed"

if 'no_gen_img' not in st.session_state:
    st.session_state.no_gen_img = 0

    if not os.path.exists(config.GEN_IMG_DIR):
        os.makedirs(config.GEN_IMG_DIR)  # Tạo thư mục

if 'list_img' not in st.session_state:
    st.session_state.list_img = []

if 'canvas_key' not in st.session_state:
    st.session_state.canvas_key = str(uuid.uuid4())

if 'page' not in st.session_state:
    st.session_state.page = "home-page"


# load env vars
load_dotenv()

# config application
st.set_page_config(page_title=config.APPLICATION_NAME, layout="centered",
                   initial_sidebar_state=st.session_state.initial_sidebar_state
                   )

# custom app css
st.markdown(f'<style>{config.APP_CSS}</style>', unsafe_allow_html=True)


# nav page
page_names_to_funcs = {
    "home-page": home.show,
    "edit-image-page": edit_image.show
}

page_names_to_funcs[st.session_state.page]()
