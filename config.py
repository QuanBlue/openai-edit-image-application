# Application
APPLICATION_NAME = 'Application'

# Image
GEN_IMG_DIR = 'gen_image'
IMG_NAME_PREFIX = 'generated_image'
IMG_MAX_WIDTH = 700
IMG_MAX_HEIGH = 700

# CSS
APP_CSS = """
    header {
        visibility: hidden
    }

    .stMainBlockContainer {
        padding-top: 1rem
        padding-bottom: 1rem
    }

    div[data-testid="stSidebarNav"] {
        display: none;
    }
    """

CANVAS_CSS = """      
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
        
        div[data-testid="InputInstructions"] {
            visibility: hidden;
        }
        
        button[kind="secondary"]  {
            border: none !important;
        }
        """