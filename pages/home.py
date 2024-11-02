import streamlit as st
import utils.image_processing as img_proc
# from main import go_to_page
import utils.page_processing as pg_proc


def show():
    st.header("Application")
    prompt = st.text_input("Input your prompt:", placeholder="Prompt")
    bg_image = st.file_uploader(
        "Background image:", type=["png", "jpg"])

    # case user upload image
    if bg_image:
        img_proc.save_gen_image(bg_image)
        pg_proc.go_to_page("edit-image-page")

    # case user input prompt
    if st.button("Submit"):
        if prompt == "":
            st.warning("Please input prompt before continuing!")
        else:
            img_proc.save_gen_image("image1.jpg")
            st.session_state.prompt = prompt
            pg_proc.go_to_page("edit-image-page")
