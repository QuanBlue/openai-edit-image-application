import streamlit as st
from openai import OpenAI
import utils.image_processing as img_proc
import utils.page_processing as pg_proc
import requests
from PIL import Image
from io import BytesIO


def show():
    st.header("Application")

    # prompt input
    prompt = st.text_input("Input your prompt:", placeholder="Prompt")
    bg_image = st.file_uploader(
        "Background image:", type=["png", "jpg"])

    # case user upload image
    if bg_image:
        img_proc.save_gen_image(bg_image)
        pg_proc.go_to_page("edit-image-page")

    submit_btn_col, announce_col = st.columns([1, 5])

    # button col
    with submit_btn_col:
        submit_button = st.button("Submit")
    with announce_col:
        announce_container = st.empty()

    
    # case user input prompt
    if submit_button:
        if prompt == "":
            st.warning("Please input prompt before continuing!")
        else:
            with announce_container.container():
                with st.spinner('Generating image...'):
                    client = OpenAI()
                    response = client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )

                # save generated image
                with st.spinner('Loading image...'):
                    image_url = response.data[0].url
                    img_proc.save_gen_image(image_url)

            # go to page
            pg_proc.go_to_page("edit-image-page")

