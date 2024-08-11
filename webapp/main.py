import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Chat Application", layout="wide")

def main():
    st.title("Welcome to the Chat Application 🤘")
    st.write("""
        This application allows you to chat with an AI assistant powered by OpenAI. You have three options:
        - **ChatGPT-like Interface**: A simple chat interface where you can ask any questions. 💬
        - **Chat with Your Data**: Upload a PDF and interact with it using the AI assistant. 📅
        - **Image Generation**: Generate images using DALL-E 3. 🖼️
    """)
    st.markdown('<a href="/chat" target="_self">Go to ChatGPT-like Interface</a>', unsafe_allow_html=True)
    st.markdown('<a href="/chat_with_your_data" target="_self">Go to Chat with Your Data</a>', unsafe_allow_html=True)
    st.markdown('<a href="/image_generation" target="_self">Go to Image Generation</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    