import config
from PIL import Image
from time import sleep
import streamlit as st
from shutil import copy
from pathlib import Path
from os import path, walk, listdir, remove


def scale_image(image, width=None, height=None):
    if width and height:
        new_width = width
        new_height = height
    else:
        # resize image to maintain aspect ratio with max width and height of 700px
        max_size = (config.IMG_MAX_WIDTH, config.IMG_MAX_HEIGH)

        # calculate the new size while maintaining the aspect ratio
        image_ratio = image.width / image.height
        max_ratio = max_size[0] / max_size[1]

        if image_ratio > max_ratio:
            # image is wider than the maximum ratio
            new_width = max_size[0]
            new_height = int(max_size[0] / image_ratio)
        else:
            # image is taller than the maximum ratio
            new_height = max_size[1]
            new_width = int(max_size[1] * image_ratio)

    scaled_image = image.resize((new_width, new_height), Image.LANCZOS)
    sleep(0.5)

    return scaled_image, new_width, new_height


def delete_gen_images():
    if path.exists(config.GEN_IMG_DIR):
        # loop all image in GEN_IMG_DIR -> delete
        for filename in listdir(config.GEN_IMG_DIR):
            file_path = path.join(config.GEN_IMG_DIR, filename)
            if path.isfile(file_path):
                remove(file_path)


def remove_draw_zone(base_image, canvas_result):
    # convert canvas result to PIL rgba
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
        sleep(config.IMG_LOAD_TIME)
    except:
        # case image is http url
        import requests
        from io import BytesIO

        width = st.session_state.canvas_width
        height = st.session_state.canvas_height

        # open then scale generated image to canvas size
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            print("\n[+] Image path:", image_path)
            response = requests.get(image_path, headers=headers, timeout=20)
        except:
            pass
        
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
        # count the number of files in the folder
        file_count = sum(len(files) for _, _, files in walk(folder_path))
        return file_count
    except Exception as e:
        return None


def download_image(index, announce_container):
    # get image name
    image_path = path.join(
        config.GEN_IMG_DIR, f"{config.IMG_NAME_PREFIX}({index}).png")
    image_name = path.basename(image_path)

    # download image
    downloads_folder = str(Path.home() / "Downloads")
    destination_path = path.join(downloads_folder, image_name)
    copy(image_path, destination_path)

    # announce download success
    with announce_container:
        timeout = 2
        success_message = st.success(
            "Download success", icon=":material/task_alt:")
        sleep(timeout)
        success_message.empty()
