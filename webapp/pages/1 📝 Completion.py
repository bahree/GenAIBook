# Importing required packages
import os
import streamlit as st
import openai
import logging

from typing import List

# pip install streamlit-chat 
from streamlit_chat import message

#pip install python-dotenv
from dotenv import load_dotenv

# Loading the .env file
load_dotenv()

# Get API key from environment variable
openai.api_type = "azure"
openai.api_base = os.getenv("AOAI_ENDPOINT")
openai.api_version = "2022-12-01"
openai.api_key = os.getenv("AOAI_KEY")

# Setting page title and header
st.set_page_config(page_title="🗨️ Completion", page_icon=":robot_face:")
#st.text("🗨️ Hello")
st.markdown("<h2 style='text-align: center;'>🗨️ Completion</h2>", unsafe_allow_html=True)

# this is not helpful
#st.balloons()


# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful AI assistant and happy to talk about pets and salons in lyrics."}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []



# Sidebar
# Temperature and token slider
st.sidebar.title("Settings")
temperature_placeholder = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.8,
    step=0.1
)

tokens_placeholder = st.sidebar.slider(
    "Tokens",
    min_value=64,
    max_value=4000,
    value=256,
    step=1
)

frequency_penalty_placeholder = st.sidebar.slider(
    "Frequency penalty",
    min_value=-2.0,
    max_value=2.0,
    value=1.0,
    step=0.1
)

presence_penalty_placeholder = st.sidebar.slider(
    "Presence penalty",
    min_value=-2.0,
    max_value=2.0,
    value=1.0,
    step=0.1
)

counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f":blue[Token count:] {st.session_state['total_tokens']}")
clear_button = st.sidebar.button("Clear", key="Clear")

# reset everything
if clear_button:
    st.session_state['total_tokens'] = []
    counter_placeholder.write(f"Token count: {st.session_state['total_tokens']}")
    tokens_placeholder = 256
    temperature_placeholder = 0.8 


def generate_completion(prompt_startphrase: str):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt_startphrase,
        temperature=temperature_placeholder,
        max_tokens=tokens_placeholder,
        frequency_penalty=frequency_penalty_placeholder,
        presence_penalty=presence_penalty_placeholder,
        stop=None)
    return response


# container for chat history
response_container = st.container()

# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=False):
        user_input = st.text_area("You:", key='input', help='Enter your prompt', height=100)
        submit_button = st.form_submit_button(label='Submit')

    if submit_button and user_input:
        response = generate_completion(user_input)
        st.text_area("AI:", value=response["choices"][0]["text"], height=200, key='output')
        
