# https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app

import streamlit as st
from PIL import Image
import os
import uuid
from time import sleep
from openai import OpenAI


IMG_MAX_WIDTH = 700
IMG_MAX_HEIGH = 700
GEN_IMG_DIR = 'gen_image'
IMG_NAME_PREFIX = 'generated_image'


def scale_image(image):
    # Resize image to maintain aspect ratio with max width and height of 700px
    max_size = (IMG_MAX_WIDTH, IMG_MAX_HEIGH)

    # Calculate the new size while maintaining the aspect ratio
    image_ratio = image.width / image.height
    max_ratio = max_size[0] / max_size[1]

    if image_ratio > max_ratio:
        # Image is wider than the maximum ratio
        new_width = max_size[0]
        new_height = int(max_size[0] / image_ratio)
    else:
        # Image is taller than the maximum ratio
        new_height = max_size[1]
        new_width = int(max_size[1] * image_ratio)

    # print("start scale...", image, end="")
    scaled_image = image.resize((new_width, new_height), Image.LANCZOS)
    sleep(0.5)
    # print("end")

    return scaled_image, new_width, new_height


def delete_gen_images():
    print("[+] Delete generated images")
    if os.path.exists(GEN_IMG_DIR):
        for filename in os.listdir(GEN_IMG_DIR):
            file_path = os.path.join(GEN_IMG_DIR, filename)
            # Xóa file
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f" > deleted: {file_path}")
    else:
        print(" > not found generated images directory")


def remove_draw_zone(base_image, canvas_result):
    img_data = canvas_result.image_data
    img_pil = Image.fromarray(img_data.astype('uint8'), 'RGBA')

    image = base_image.convert('RGBA').resize(img_pil.size)

    # split alpha channel of image (opacity channel) and convert black-white mask
    alpha_channel = img_pil.split()[-1]
    mask = Image.eval(alpha_channel, lambda a: 255 if a == 0 else 0)

    # remove draw zone in base image
    removed_image = Image.composite(image, Image.new(
        'RGBA', image.size, (0, 0, 0, 0)), mask)

    return removed_image


def load_image(image_path):
    try:
        # case image is local path
        img = Image.open(image_path)
        sleep(1)
    except:
        # case image is http url
        import requests
        from io import BytesIO

        response = requests.get(image_path)
        img = Image.open(BytesIO(response.content))

    return img


def save_gen_image(image):
    import re

    try:
        # case image is local path or http url
        image = load_image(image)
    except:
        # case image is PNG/JPG/... type (pass)
        pass

    st.session_state.no_gen_img += 1
    image_save_path = os.path.join(
        GEN_IMG_DIR, f"{IMG_NAME_PREFIX}({st.session_state.no_gen_img}).png")

    # remove image have index greater than st.session_state.no_gen_img
    for filename in os.listdir(GEN_IMG_DIR):
        # Kiểm tra nếu tên tệp phù hợp với định dạng "image_{num}.png"
        pattern = re.compile(rf"{IMG_NAME_PREFIX}\((\d+)\)\.png")
        match = pattern.match(filename)

        if match:
            num = int(match.group(1))
            if num >= st.session_state.no_gen_img:
                file_path = os.path.join(GEN_IMG_DIR, filename)
                os.remove(file_path)

    # remove image have index greater than st.session_state.no_gen_img in image list
    st.session_state.list_img = st.session_state.list_img[:st.session_state.no_gen_img - 1]

    # save gen image
    st.session_state.list_img.append(image)
    image.save(image_save_path)


def count_files_in_folder(folder_path):
    try:
        # Đếm số file trong folder
        file_count = sum(len(files) for _, _, files in os.walk(folder_path))
        return file_count
    except Exception as e:
        print(f"Error: {e}")
        return None


def download_image(index):
    from shutil import copy
    from pathlib import Path

    # Lấy tên file từ đường dẫn
    image_path = os.path.join(
        GEN_IMG_DIR, f"{IMG_NAME_PREFIX}({index}).png")
    image_name = os.path.basename(image_path)

    # Download
    downloads_folder = str(Path.home() / "Downloads")
    destination_path = os.path.join(downloads_folder, image_name)
    copy(image_path, destination_path)

    # st.success("download success")


def next_image():
    st.session_state.no_gen_img += 1
    st.rerun()
    print("Next image:", st.session_state.no_gen_img)


def prev_image():
    st.session_state.no_gen_img -= 1
    print("Prev image:", st.session_state.no_gen_img)


def prompt_input_page():
    import streamlit as st

    st.header("Application")
    prompt = st.text_input("Input your prompt:", placeholder="Prompt")
    bg_image = st.file_uploader(
        "Background image:", type=["png", "jpg"])

    # case user upload image
    if bg_image:
        save_gen_image(bg_image)
        go_to_page("edit-image-page")

    # case user input prompt
    if st.button("Submit"):
        if prompt == "":
            st.warning("Please input prompt before continuing!")
        else:
            save_gen_image("image1.jpg")
            st.session_state.prompt = prompt
            go_to_page("edit-image-page")


def edit_image_page():
    import uuid
    from streamlit_drawable_canvas import st_canvas

    print(">>>>>>>>>>>> edit image")
    print("image no:", st.session_state.no_gen_img)
    print("len list_img:", len(st.session_state.list_img))
    canvas_css = """
        header {
            visibility: hidden;
        }
        
        .stMainBlockContainer {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
        div[data-testid="stSidebarHeader"] {
            height: 0px !important;       
            padding: 5px;     
        }
        
        .stMarkdown {
            display: grid;
            place-items: center;
        }
        
        .stHorizontalBlock {
            display: flex; justify-content: center; align-items: center; height: 100%;
        }
        
        button[kind="secondary"]  {
            border: none !important;
        }
        """

    st.markdown(f'<style>{canvas_css}</style>', unsafe_allow_html=True)

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
                # st.session_state.scaled_gen_image, st.session_state.canvas_width, st.session_state.canvas_height = scale_image(
                #     canvas_result)

                # print("canvas result sz:", canvas_result.size())
                current_gen_image = st.session_state.list_img[st.session_state.no_gen_img - 1]
                # print("current_gen_image sz:", current_gen_image.size())
                current_img_path = os.path.join(
                    GEN_IMG_DIR, f"{IMG_NAME_PREFIX}({st.session_state.no_gen_img}).png")
                removed_image = remove_draw_zone(
                    current_gen_image, canvas_result)
                # print("current_gen_image sz:", current_gen_image.size())

                removed_image.save("removed_image.png")
                st.session_state.scaled_gen_image.save("base_image.png")

                client = OpenAI()
                response = client.images.edit(
                    model="dall-e-2",
                    image=open("base_image.png", 'rb'),
                    mask=open("removed_image.png", 'rb'),
                    prompt=change_prompt,
                    n=1,
                )
                image_url = response.data[0].url
                print("image url:", image_url)

                save_gen_image(image_url)

                # Reset image
                st.session_state.canvas_result = None
                st.session_state.scaled_gen_image = None
                st.session_state.canvas_key = str(uuid.uuid4())

        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("New Project", type="primary", use_container_width=True):
            print("[+] New project")
            print(" > clear session state...", end="")
            st.session_state.clear()
            print("done")
            print(" > clear cache data...", end="")
            st.cache_data.clear()
            print("done")

            st.session_state.canvas_key = str(uuid.uuid4())
            delete_gen_images()
            go_to_page("home-page")

    with st.spinner("Processing..."):
        # Load image
        no_gen_img = st.session_state.no_gen_img
        gen_image = st.session_state.list_img[no_gen_img - 1]

    success_placeholder = st.empty()
    success_placeholder.success("Done")
    success_placeholder.empty()

    st.session_state.scaled_gen_image, st.session_state.canvas_width, st.session_state.canvas_height = scale_image(
        gen_image)

    col1, col2, _, _ = st.columns([2, 1, 5, 5])

    with col1:
        stroke_width = st.slider(
            ">", 1, 100, 25, format="", label_visibility="collapsed")
    with col2:
        if st.button(">", icon=":material/download:", help="Download Image", use_container_width=True):
            download_image(st.session_state.no_gen_img)

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

    button_col1, text_col2, button_col3, _ = st.columns([1, 2, 1, 20])
    # View Previous image
    with button_col1:
        st.button(">", on_click=prev_image, icon=":material/chevron_left:", help="Previous image",
                  key="view_prev_image", use_container_width=True, disabled=(st.session_state.no_gen_img == 1))
    with text_col2:
        no_of_current_image = st.session_state.no_gen_img
        number_of_image_generated = count_files_in_folder(GEN_IMG_DIR)
        st.write(f"{no_of_current_image}/{number_of_image_generated}")
    # View Next image
    with button_col3:
        st.button(">", on_click=next_image, icon=":material/chevron_right:", help="Next image", key="view_next_image",
                  use_container_width=True, disabled=(st.session_state.no_gen_img == number_of_image_generated))


st.set_page_config(page_title="Application", layout="centered",
                   initial_sidebar_state="auto")

page_names_to_funcs = {
    "home-page": prompt_input_page,
    "edit-image-page": edit_image_page
}


def go_to_page(page_name):
    if st.session_state.get("page") != page_name:
        print("[+] Go to page:", page_name)
        st.session_state.page = page_name
        st.rerun()


if 'page' not in st.session_state:
    st.session_state.page = "home-page"

if 'no_gen_img' not in st.session_state:
    st.session_state.no_gen_img = 0

    print("[+] Create generated images directory")
    if not os.path.exists(GEN_IMG_DIR):
        os.makedirs(GEN_IMG_DIR)  # Tạo thư mục
        print(f" > directory '{GEN_IMG_DIR}' created")
    else:
        print(f" > directory '{GEN_IMG_DIR}' already exist.")

if 'list_img' not in st.session_state:
    st.session_state.list_img = []

if 'canvas_key' not in st.session_state:
    st.session_state.canvas_key = str(uuid.uuid4())


page_names_to_funcs[st.session_state.page]()
