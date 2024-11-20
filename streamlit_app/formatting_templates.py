import base64
import streamlit as st

LOGO_PATH = r"streamlit_app\logo.jpg"  
def load_logo(logo_path):
    with open(logo_path, "rb") as img_file:
        encoded_img = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{encoded_img}"
LOGO_URL = load_logo(LOGO_PATH)

def load_css():
    st.markdown("""
        <style>
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background: linear-gradient(90deg, #f8f9fa 0%, #ffffff 100%);
            border-radius: 10px;
            box-shadow: 0 0px 0 1px rgba(0,0,0,0.07);
            margin-bottom: 2rem;
        }
        
        .logo-title-container {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .app-logo {
            width: 80px;
            height: 80px;
            object-fit: contain;
            border-radius: 100%;
        }
        
        .app-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #2D2D2D;
            margin: 0;
            font-family: 'Source Sans Pro', sans-serif;
        }
        
        .clear-button {
            background-color: #FF4B4B;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            font-weight: 600;
            transition: background-color 0.3s;
        }
        
        .clear-button:hover {
            background-color: #FF3333;
        }

        /* chat styling */
        .stChatMessage {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            max-width: 75%;
            word-wrap: break-word;
            margin-left: 10px;
            margin-right: 10px;
        }

        .stChatInput {
            border-radius: 20px;
            border: 2px solid #e9ecef;
            padding: 0.5rem 1rem;
            width: max-content; /* Make sure the input is responsive */
            margin: 0 10px;
        }

        .stExpander {
            border: none;
            background-color: transparent;
        }

        /* align chat container */
        .stContainer {
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
        }
        
        /* Hide Streamlit's default header */
        # #MainMenu {visibility: hidden;}
        # header {visibility: hidden;}
        # footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def custom_header():
    header_html = f'''
    <div class="header-container">
        <div class="logo-title-container">
            <img src="{LOGO_URL}" class="app-logo" alt="Perplexio Logo"/>
            <h1 class="app-title">Perplexio - Your AI Assistant</h1>
        </div>
        <div>
            <form method="get">
                <button class="clear-button" type="submit" name="clear_chat">Clear Chat</button>
            </form>
        </div>
    </div>
    '''
    st.markdown(header_html, unsafe_allow_html=True)

    if "clear_chat" in st.query_params:
        st.session_state.chat_history = []
        st.session_state.url_history = []
        st.query_params.clear()
        st.rerun()