# Importing required packages
import os
import streamlit as st
import openai
import logging
import requests
import json
import datetime
import re

from typing import List

#pip install python-dotenv
from dotenv import load_dotenv

# Loading the .env file
load_dotenv()

# Setting page title and header
st.set_page_config(page_title="🖼️ Image Generation", page_icon=":robot_face:")
#st.text("🖼️ Image Generation")
st.markdown("<h1 style='text-align: center;'>🖼️ Image Generation</h1>", unsafe_allow_html=True)

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

# Sidebar
st.sidebar.title("Settings")

api_endpoint = st.sidebar.radio(
    "API",
    ("Azure OpenAI", "OpenAI"),
    index=1
)

if api_endpoint == "Azure OpenAI":
    image_count = st.sidebar.slider(
        "Images to generate",
        min_value=1,
        max_value=5,
        value=1
    )
else:
    image_count = st.sidebar.slider(
        "Images to generate",
        min_value=1,
        max_value=10,
        value=1
    )

image_size = st.sidebar.radio(
    "Image size",
    ("256x256", "512x512", "1024x1024"),
    index=2
)

debug = st.sidebar.checkbox('Debug', key='debug')

if api_endpoint == "Azure OpenAI":
    openai.api_type = "azure"
    openai.api_base = os.getenv("AOAI_ENDPOINT")
    #openai.api_version = "2022-12-01"
    openai.api_version = "2023-06-01-preview"
    openai.api_key = os.getenv("AOAI_KEY")
else:
    openai.api_type="open_ai"
    openai.api_key = os.getenv("OPENAI_API_BOOK_KEY")
    openai.organization = os.getenv("OPENAI_API_BOOK_ORG")
    
    
if(debug):
    if api_endpoint == "Azure OpenAI":
        api_settings = st.sidebar.expander("Azure OpenAI Settings", expanded=False)
        api_settings.write(f"API key: ```{openai.api_key}```")
        api_settings.write(f"Endpoint: ```{openai.api_base}```")
        api_settings.write(f"Version: ```{openai.api_version}```")
    else:
        api_settings = st.sidebar.expander("OpenAI Settings", expanded=False)
        api_settings.write(f"API key: ```{openai.api_key}```")
        api_settings.write(f"Org: ```{openai.organization}```")

clear_button = st.sidebar.button("Clear", key="Clear")

# reset everything
if clear_button:
    st.session_state['generated'] = []
    image_count = 1
    image_size = "1024x1024"
    api_endpoint = "Azure OpenAI"
    api_settings.clear()

# Call the DALL-E API
def dalle_generate_images(prompt_startphrase: str):
    response = openai.Image.create(
        prompt=prompt_startphrase,
        n=image_count,
        size=image_size
    )
    return response

# Function to clean up filenames
def valid_filename(s):
    s = re.sub(r'[^\w_.)( -]', '', s).strip()
    return re.sub(r'[\s]+', '_', s)

with st.expander("See explanation"):
    st.write("Generative AI may produce inaccurate information about people, places, or facts. Please check your results carefully and do not regard them as trustworthy.")

# container for text box
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=False):
        # Get the prompt from the user
        input_prompt = st.text_area("Image generation prompt:", key='input', help='Enter your prompt:', height=100)
        submit_button = st.form_submit_button(label='Submit')

    if submit_button and input_prompt:
        #response = openai.Image.create(prompt=input_prompt, n=1,size="1024x1024")
        response = dalle_generate_images(input_prompt)
        st.toast('Your image(s) were genrated!', icon='😍')
        
        # Store the response in the session state
        st.session_state['generated'].append(response)
        
        # If debug is enabled, show the raw API response
        if debug:
            st.text_area(f"**Response**", value=response, height=200)
        
        # Loop through the images and display them
        for i, item_image in enumerate(response['data']):
            if debug:
                #st.text_area(f"**Image {i+1} URL:**", value=item_image['url'], height=200)
                st.markdown(f"[***Link Image {i+1}***]({item_image['url']})")
            
            # Download the image
            image = requests.get(item_image['url']).content
            
            # Display the image
            st.image(image)
            
            # Generate a filename and download button
            filename = f"{valid_filename(input_prompt)}_{i+1}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            st.download_button(f'**Download Image {i+1}**', image, file_name=filename, mime='image/png', on_click=lambda: None,help=f"Download image {i+1}")
            
        # image_url = response['data'][0]['url']
        # #st.text_area("Image URL", value=image_url, height=200, key='output')
        # st.text_area("Image URL", value=response, height=200, key='output')
        # image = requests.get(image_url).content
        # st.image(image)
        # st.toast('Your edited image was saved!', icon='😍')
        
        # #filename = f"dalle_image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        # filename = f"{valid_filename(input_prompt)}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        # st.download_button('Download image', image, file_name=filename, mime='image/png')
        

# {
#   "created": 1690501153,
#   "data": [
#     {
#       "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-rocrupyvzgcl4yf25rqq6d1v/user-oerSg9brH81sl0JtN11UxceP/img-MMYYPAcRsQ60bgxa3maftOnh.png?st=2023-07-27T22%3A39%3A13Z&se=2023-07-28T00%3A39%3A13Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-07-27T15%3A32%3A00Z&ske=2023-07-28T15%3A32%3A00Z&sks=b&skv=2021-08-06&sig=4Q9Pipt%2BXD8W0y5DBflE24PqRwi5fQkuMI7x5lwsMy0%3D"
#     },
#     {
#       "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-rocrupyvzgcl4yf25rqq6d1v/user-oerSg9brH81sl0JtN11UxceP/img-lmUN34AYetng34gk7xe27ypY.png?st=2023-07-27T22%3A39%3A13Z&se=2023-07-28T00%3A39%3A13Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-07-27T15%3A32%3A00Z&ske=2023-07-28T15%3A32%3A00Z&sks=b&skv=2021-08-06&sig=Rs20LSUjbXfxi9cMU2mooUcmoIyqkQtbMMCAo9bsP0E%3D"
#     },
#     {
#       "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-rocrupyvzgcl4yf25rqq6d1v/user-oerSg9brH81sl0JtN11UxceP/img-4fPae8Andfrj9PKxX1Dop97e.png?st=2023-07-27T22%3A39%3A13Z&se=2023-07-28T00%3A39%3A13Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-07-27T15%3A32%3A00Z&ske=2023-07-28T15%3A32%3A00Z&sks=b&skv=2021-08-06&sig=nXM8ZJT1JfR1m7Nm6AHeFkul0HAGLJpyQITtXVGhdW8%3D"
#     }
#   ]
# }