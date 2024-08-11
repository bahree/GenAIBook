import streamlit as st
from openai import OpenAI, AzureOpenAI
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Define API key variables
openai_api_key = os.getenv("OPENAI_API_KEY")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
openai_model_name = os.getenv("OPENAI_MODEL_NAME")
azure_openai_model_name = os.getenv("AZURE_OPENAI_MODEL_NAME")

# Initialize OpenAI or Azure OpenAI based on selection
def initialize_openai(api_choice):
    if api_choice == 'OpenAI':
        return OpenAI(api_key=openai_api_key)
    elif api_choice == 'AzureOpenAI':
        return AzureOpenAI(
            azure_endpoint=azure_openai_endpoint,
            api_version=azure_openai_api_version,
            api_key=azure_openai_api_key
        )

# Get the model name based on the API choice
def get_model_name(api_choice):
    if api_choice == 'OpenAI':
        return openai_model_name
    elif api_choice == 'AzureOpenAI':
        return azure_openai_model_name

# Shared sidebar settings
def sidebar_settings():
    st.sidebar.header("Settings")
    api_choice = st.sidebar.selectbox("Choose API", ["OpenAI", "AzureOpenAI"])
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.sidebar.slider("Max Tokens", 10, 32000, 800)

    st.session_state.api_choice = api_choice
    st.session_state.temperature = temperature
    st.session_state.max_tokens = max_tokens

def chat_interface():
    st.title("ChatGPT-like Interface 💬")
    
    sidebar_settings()
    
    client = initialize_openai(st.session_state.api_choice)
    model_name = get_model_name(st.session_state.api_choice)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "system", "content": "You are an AI assistant that helps people find information."}]

    user_input = st.chat_input("You: ")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model=model_name,
            messages=st.session_state.chat_history,
            temperature=st.session_state.temperature,
            max_tokens=st.session_state.max_tokens
        )
        
        st.session_state.chat_history.append({"role": "assistant", "content": response.choices[0].message.content.strip()})

    if st.button("Clear Chat History"):
        st.session_state.chat_history = [{"role": "system", "content": "You are an AI assistant that helps people find information."}]
    
    for message in st.session_state.chat_history:
        if message["role"] != "system":
            st.chat_message(message['role']).write(message['content'])

if __name__ == "__main__":
    chat_interface()
