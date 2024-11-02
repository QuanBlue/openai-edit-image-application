
import streamlit as st


def go_to_page(page_name):
    if st.session_state.get("page") != page_name:
        st.session_state.page = page_name
        st.rerun()
