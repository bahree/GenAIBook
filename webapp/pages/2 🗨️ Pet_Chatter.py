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
openai.api_version = "2023-05-15"
#openai.api_version = "2023-06-01-preview"
openai.api_key = os.getenv("AOAI_KEY")

# Setting page title and header
st.set_page_config(page_title="🗨️ Hello", page_icon=":robot_face:")
st.text("🗨️ Pet Chatter")
st.markdown("<h1 style='text-align: center;'>🗨️ Pet Chatter</h1>", unsafe_allow_html=True)


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

# this is not helpful
# st.snow()

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

model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Token count: {st.session_state['total_tokens']}")
clear_button = st.sidebar.button("Clear", key="Clear")

# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "turbo"
else:
    model = "gpt4-32k-613"

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful AI assistant and happy to talk about pets and salons in lyrics."}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['total_tokens'] = []
    counter_placeholder.write(f"Token count: {st.session_state['total_tokens']}")
    tokens_placeholder = 256
    temperature_placeholder = 0.8 

# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        #engine="turbo",
        engine=model,
        temperature=temperature_placeholder,
        max_tokens=tokens_placeholder,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens


# if st.button('Say hello'):
#     st.write('Why hello there', temperature_placeholder)
# else:
#     st.write('Goodbye')
# st.write(temperature_placeholder)

# txt = st.text_area('Text to analyze', '''
#     It was the best of times, it was the worst of times, it was
#     the age of wisdom, it was the age of foolishness, it was
#     the epoch of belief, it was the epoch of incredulity, it
#     was the season of Light, it was the season of Darkness, it
#     was the spring of hope, it was the winter of despair, (...)
#     ''')


# container for chat history
response_container = st.container()

# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', help='Enter your prompt', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
            st.write(f"Token count: {st.session_state['total_tokens'][i]}")
            counter_placeholder.write(f"Token count: {st.session_state['total_tokens'][i]}")