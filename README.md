<h1 align="center">
  <img src="./assets/facebook-logo.png" alt="icon" width="200"></img>
  <br>
  <b>Edit image application by OpenAI</b>
</h1>

<p align="center">Edit image application by <b>OpenAI API</b>.</p>

<!-- Badges -->
<p align="center">
  <a href="https://github.com/QuanBlue/openai-edit-image-application/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/QuanBlue/openai-edit-image-application" alt="contributors" />
  </a>
  <a href="">
    <img src="https://img.shields.io/github/last-commit/QuanBlue/openai-edit-image-application" alt="last update" />
  </a>
  <a href="https://github.com/QuanBlue/openai-edit-image-application/network/members">
    <img src="https://img.shields.io/github/forks/QuanBlue/openai-edit-image-application" alt="forks" />
  </a>
  <a href="https://github.com/QuanBlue/openai-edit-image-application/stargazers">
    <img src="https://img.shields.io/github/stars/QuanBlue/openai-edit-image-application" alt="stars" />
  </a>
  <a href="https://github.com/QuanBlue/openai-edit-image-application/issues/">
    <img src="https://img.shields.io/github/issues/QuanBlue/openai-edit-image-application" alt="open issues" />
  </a>
  <a href="https://github.com/QuanBlue/openai-edit-image-application/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/QuanBlue/openai-edit-image-application.svg" alt="license" />
  </a>
</p>

<p align="center">
  <b>
      <a href="https://github.com/QuanBlue/openai-edit-image-application">Documentation</a> •
      <a href="https://github.com/QuanBlue/openai-edit-image-application/issues/">Report Bug</a> •
      <a href="https://github.com/QuanBlue/openai-edit-image-application/issues/">Request Feature</a>
  </b>
</p>

<br/>

<details open>
<summary><b>📖 Table of Contents</b></summary>

- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Run Locally](#run-locally)
- [Contributors](#contributors)
- [Credits](#credits)
- [Reference](#reference)
- [License](#license)
</details>

# Key Features

-  **Generate image:** allow user to generate image by input prompt
-  **Edit image:** allow user to edit image by draw zone want edit then input prompt what you want to edit

# Tech Stack

-  **Application**: streamlit
-  **API**: OpenAI API

# Getting Started

## Project Structure

```txt
.

├── pages
│   ├── edit_image.py
│   └── home.py
├── utils
│   ├── image_processing.py
│   └── page_processing.py
├── config.py
├── main.py
├── .env
├── requirements.txt
└── README.md
```

## Prerequisites

-  **Python:** `>= 3.10.7`. Install [here](https://www.python.org/downloads/).
-  **Package**: OpenAI, Streamlit,... Install by run the following command:
   ```sh
   pip install -r requirements.txt
   ```

## Environment Variables

To run this project, you need to add the following environment variables to your `.env` :

-  **Application configs:** Create `.env` file in `./`

   -  `OPENAI_API_KEY`: API key of OpenAI.
      > Check [How to get OpenAI API](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key) to know how to get OpenAI API.

   Example:

   ```sh
   # .env
   #  OpenAI API key
   OPENAI_API_KEY=sk-proj-u0Hj9VdFBS...0_AF5_z2Cq7ky6-ovcqaAyriMA
   ```

You can also check out the file `.env.example` to see all required environment variables.

## Run Locally

Clone project

```bash
git clone https://github.com/QuanBlue/openai-edit-image-application.git
```

> **Note**
> If you're using Linux Bash for Windows, [see this guide](https://www.howtogeek.com/261575/how-to-run-graphical-linux-desktop-applications-from-windows-10s-bash-shell/) or use `node` from the command prompt.

Run application

```bash
streamlit run ./main.py
```

# Contributors

<a href="https://github.com/QuanBlue/openai-edit-image-application/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=QuanBlue/openai-edit-image-application" />
</a>

Contributions are always welcome!

# Credits

This software uses the following packages:

-  Streamlit [here](https://streamlit.io/)
-  OpenAI API [here](https://openai.com/index/openai-api/)
-  Application icon [here](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)

# Reference

-  Quick start OpenAI [here](https://platform.openai.com/docs/quickstart)
-  OpenAI guide - How to generate image [here](https://platform.openai.com/docs/guides/images)
-  Edit image with dall-e [here](https://help.openai.com/en/articles/9055440-editing-your-images-with-dall-e)

# License

Distributed under the MIT License. See <a href="./LICENSE">`LICENSE`</a> for more information.

---

> Bento [@quanblue](https://bento.me/quanblue) &nbsp;&middot;&nbsp;
> GitHub [@QuanBlue](https://github.com/QuanBlue) &nbsp;&middot;&nbsp; Gmail quannguyenthanh558@gmail.com
