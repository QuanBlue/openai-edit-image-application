from shutil import copy
from pathlib import Path
import config
from PIL import Image
from time import sleep
from os import path, walk, listdir, remove
import streamlit as st


def scale_image(image, width=None, height=None):
    if width and height:
        new_width = width
        new_height = height
    else:
        # Resize image to maintain aspect ratio with max width and height of 700px
        max_size = (config.IMG_MAX_WIDTH, config.IMG_MAX_HEIGH)

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

    scaled_image = image.resize((new_width, new_height), Image.LANCZOS)
    sleep(0.5)

    return scaled_image, new_width, new_height


def delete_gen_images():
    if path.exists(config.GEN_IMG_DIR):
        for filename in listdir(config.GEN_IMG_DIR):
            file_path = path.join(config.GEN_IMG_DIR, filename)
            # Xóa file
            if path.isfile(file_path):
                remove(file_path)


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

        width = st.session_state.canvas_width
        height = st.session_state.canvas_height

        response = requests.get(image_path)
        img = Image.open(BytesIO(response.content))
        img, _, _ = scale_image(img, width, height)

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
    image_save_path = path.join(
        config.GEN_IMG_DIR, f"{config.IMG_NAME_PREFIX}({st.session_state.no_gen_img}).png")

    # remove image have index greater than st.session_state.no_gen_img
    for filename in listdir(config.GEN_IMG_DIR):
        # Kiểm tra nếu tên tệp phù hợp với định dạng "image_{num}.png"
        pattern = re.compile(rf"{config.IMG_NAME_PREFIX}\((\d+)\)\.png")
        match = pattern.match(filename)

        if match:
            num = int(match.group(1))
            if num >= st.session_state.no_gen_img:
                file_path = path.join(config.GEN_IMG_DIR, filename)
                remove(file_path)

    # remove image have index greater than st.session_state.no_gen_img in image list
    st.session_state.list_img = st.session_state.list_img[:st.session_state.no_gen_img - 1]

    # save gen image
    st.session_state.list_img.append(image)
    image.save(image_save_path)


def count_files_in_folder(folder_path):
    try:
        # Đếm số file trong folder
        file_count = sum(len(files) for _, _, files in walk(folder_path))
        return file_count
    except Exception as e:
        return None


def download_image(index, announce_container):
    # Lấy tên file từ đường dẫn
    image_path = path.join(
        config.GEN_IMG_DIR, f"{config.IMG_NAME_PREFIX}({index}).png")
    image_name = path.basename(image_path)

    # Download
    downloads_folder = str(Path.home() / "Downloads")
    destination_path = path.join(downloads_folder, image_name)
    copy(image_path, destination_path)

    with announce_container:
        timeout = 2
        success_message = st.success(
            "Download success", icon=":material/task_alt:")
        sleep(timeout)
        success_message.empty()
