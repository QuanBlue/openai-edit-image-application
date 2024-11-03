import uuid
import config
from openai import OpenAI
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import utils.image_processing as img_proc
import utils.page_processing as pg_proc


def next_image():
    st.session_state.no_gen_img += 1
    st.rerun()


def prev_image():
    st.session_state.no_gen_img -= 1


def show():
    # custom page css
    st.markdown(f'<style>{config.CANVAS_CSS}</style>', unsafe_allow_html=True)

    # expand sidebar
    st.session_state.initial_sidebar_state = "expanded"

    # sidebar
    with st.sidebar:
        st.header("Application")

        # edit image prompt input
        input_col1, input_col2 = st.columns(
            [4, 1], vertical_alignment="bottom")
        with input_col1:
            change_prompt = st.text_input("Describing your changes:",
                                          placeholder="Edit image...")
        with input_col2:
            if st.button(">", icon=":material/send:"):
                # remove draw zone in image
                canvas_result = st.session_state.canvas_result
                current_gen_image = st.session_state.list_img[st.session_state.no_gen_img - 1]
                removed_image = img_proc.remove_draw_zone(
                    current_gen_image, canvas_result)

                # save base image and mask
                removed_image.save("removed_image.png")
                st.session_state.scaled_gen_image.save("base_image.png")

                # call OpenAI API
                client = OpenAI()
                response = client.images.edit(
                    model="dall-e-2",
                    image=open("base_image.png", 'rb'),
                    mask=open("removed_image.png", 'rb'),
                    prompt=change_prompt,
                    n=1,
                )

                # save generated image
                image_url = response.data[0].url
                img_proc.save_gen_image(image_url)

                # reset canvas
                st.session_state.canvas_result = None
                st.session_state.scaled_gen_image = None
                st.session_state.canvas_key = str(uuid.uuid4())

        st.markdown("<br><br>", unsafe_allow_html=True)

        # new project button
        if st.button("New Project", type="primary", use_container_width=True):
            # clear session + generated images
            st.session_state.clear()
            st.session_state.canvas_key = str(uuid.uuid4())
            img_proc.delete_gen_images()

            # go to homepage
            pg_proc.go_to_page("home-page")

    # load image
    with st.spinner("Processing..."):
        try:
            no_gen_img = st.session_state.no_gen_img
            gen_image = st.session_state.list_img[no_gen_img - 1]
        except:
            gen_image = None

    # success announce
    success_placeholder = st.empty()
    success_placeholder.success("Done")
    success_placeholder.empty()

    # scale gen image
    st.session_state.scaled_gen_image, st.session_state.canvas_width, st.session_state.canvas_height = img_proc.scale_image(
        gen_image)

    # edit option tools
    brush_sz_col, download_btn_col, announce_col, _ = st.columns([2, 1, 5, 5])
    with brush_sz_col:
        stroke_width = st.slider(
            ">", 1, 150, 50, format="", label_visibility="collapsed")
    with announce_col:
        announce_container = st.container()
    with download_btn_col:
        if st.button(">", icon=":material/download:", help="Download Image", use_container_width=True):
            img_proc.download_image(
                st.session_state.no_gen_img, announce_container)

    # canvas
    st.session_state.canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color="rgba(65, 150, 180, 0.5)",
        background_image=st.session_state.scaled_gen_image,
        width=st.session_state.canvas_width,
        height=st.session_state.canvas_height,
        drawing_mode="freedraw",
        display_toolbar=False,
        key=st.session_state.canvas_key
    )

    # image view nav
    next_img_col, img_no_col, prev_img_col, _ = st.columns([1, 2, 1, 20])
    with next_img_col:
        st.button(">", on_click=prev_image, icon=":material/chevron_left:", help="Previous image",
                  key="view_prev_image", use_container_width=True, disabled=(st.session_state.no_gen_img == 1))
    with img_no_col:
        no_of_current_image = st.session_state.no_gen_img
        number_of_image_generated = img_proc.count_files_in_folder(
            config.GEN_IMG_DIR)
        st.write(f"{no_of_current_image}/{number_of_image_generated}")
    with prev_img_col:
        st.button(">", on_click=next_image, icon=":material/chevron_right:", help="Next image", key="view_next_image",
                  use_container_width=True, disabled=(st.session_state.no_gen_img == number_of_image_generated))
