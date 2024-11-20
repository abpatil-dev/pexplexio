import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
import requests
import json
from formatting_templates import load_css, custom_header

BACKEND_URL = "http://localhost:5000/api/chat"

def main():
    st.set_page_config(
        page_title="Perplexio",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            'Get Help': 'https://www.your-help-url.com',
            'Report a bug': 'https://www.your-bug-report-url.com',
            'About': 'Perplexio - Your AI Assistant'
        }
    )
    load_css()
    custom_header()
    

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'url_history' not in st.session_state:
        st.session_state.url_history = []
    if 'pending_response' not in st.session_state:
        st.session_state.pending_response = False

    chat_container = st.container()
    
    with chat_container:
        for i in range(len(st.session_state.chat_history)):
            message = st.session_state.chat_history[i]
            urls = st.session_state.url_history[i] if i < len(st.session_state.url_history) else []

            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.write(message.content)
            else:
                with st.chat_message("assistant"):
                    st.write(message.content)
                    if urls:
                        with st.expander(f"Reference URLs (Total: {len(urls)})"):
                            for j, url in enumerate(urls, 1):
                                st.markdown(f"{j}. [{url}]({url})")

        if st.session_state.pending_response:
            with st.spinner('Generating response...'):
                serializable_history = []
                for msg in st.session_state.chat_history:
                    if isinstance(msg, HumanMessage):
                        serializable_history.append({
                            'role': 'human',
                            'content': msg.content
                        })
                    else:
                        serializable_history.append({
                            'role': 'assistant',
                            'content': msg.content
                        })

                response = requests.post(
                    BACKEND_URL,
                    json={
                        'user_input': st.session_state.chat_history[-1].content,
                        'chat_history': serializable_history
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data['response']
                    urls = data['urls']
                else:
                    ai_response = "Sorry, there was an error processing your request."
                    urls = []

            st.session_state.chat_history.append(AIMessage(content=ai_response))
            st.session_state.url_history.append(urls)
            st.session_state.pending_response = False
            st.rerun()

    if user_input := st.chat_input("Type your message here..."):
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        st.session_state.url_history.append([])
        st.session_state.pending_response = True
        st.rerun()

if __name__ == '__main__':
    main()