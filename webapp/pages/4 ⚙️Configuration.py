# Importing required packages
import os
import streamlit as st
import openai
import logging
import requests
import json
import datetime

from typing import List

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
st.set_page_config(page_title="⚙️ Setting", page_icon=":robot_face:")
#st.text("⚙️ Setting")
st.markdown("<h1 style='text-align: center;'>⚙️ Setting</h1>", unsafe_allow_html=True)


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
openai_settings = st.sidebar.expander("OpenAI Settings", expanded=False)
openai_settings.write(f"Type: {openai.api_type}")
openai_settings.write(f"API key: {openai.api_key}")
openai_settings.write(f"Endpoint: {openai.api_base}")
openai_settings.write(f"API Version: {openai.api_version}")
openai_settings.write(f"Org: {openai.organization}")

# We can consider this version
st.sidebar.markdown(f"API Key: ```{openai.api_key}```", unsafe_allow_html=True)

# # adding a text input widget to the sidebar
# openai.organization = st.sidebar.text_input('Enter your Org:')
# add_textbox = st.sidebar.text_input('Enter your Key:')

# # Temperature and token slider
# st.sidebar.title("Settings")
# temperature_placeholder = st.sidebar.slider(
#     "Temperature",
#     min_value=0.0,
#     max_value=2.0,
#     value=0.8,
#     step=0.1
# )

# tokens_placeholder = st.sidebar.slider(
#     "Tokens",
#     min_value=64,
#     max_value=4000,
#     value=256,
#     step=1
# )

# counter_placeholder = st.sidebar.empty()
# counter_placeholder.write(f"Token count: {st.session_state['total_tokens']}")
# clear_button = st.sidebar.button("Clear", key="Clear")

# # reset everything
# if clear_button:
#     st.session_state['total_tokens'] = []
#     counter_placeholder.write(f"Token count: {st.session_state['total_tokens']}")
#     tokens_placeholder = 256
#     temperature_placeholder = 0.8 

st.caption('This is a string that explains something above.')
st.caption('A caption with _italics_ :blue[colors] and emojis :sunglasses:')


# container for text box
container = st.container()

import streamlit as st

text = st.text_area("Enter some text", value="", height=200)
markdown_text = f"### Here is the text you entered:\n\n{text}"
st.markdown(markdown_text)


# with container:
#     with st.form(key='my_form', clear_on_submit=False):
#         user_input = st.text_area("You:", key='input', help='Enter your prompt', height=100)
#         submit_button = st.form_submit_button(label='Send')

#     if submit_button and user_input:
#         response = generate_completion(user_input)
#         st.text_area("AI:", value=response["choices"][0]["text"], height=200, key='output')



# with container:
#     with st.form(key='my_form', clear_on_submit=True):
#         user_input = st.text_area("You:", key='input', help='Enter your prompt', height=100)
#         submit_button = st.form_submit_button(label='Send')

#     if submit_button and user_input:
#         response = generate_completion(user_input)
#         st.text_area("AI:", value=response["choices"][0]["text"], height=200, key='output')
        
# if st.session_state['generated']:
#     with response_container:
#         for i in range(len(st.session_state['generated'])):
#             message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
#             message(st.session_state["generated"][i], key=str(i))
#             st.write(f"Token count: {st.session_state['total_tokens'][i]}")
#             counter_placeholder.write(f"Token count: {st.session_state['total_tokens'][i]}")