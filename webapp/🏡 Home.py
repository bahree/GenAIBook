# Importing required packages
import os
import streamlit as st
import openai
import logging

from typing import List

# Setting page title and header
st.set_page_config(page_title="🗨️ Hello", page_icon=":robot_face:")
#st.text("🗨️ Hello")
st.markdown("<h1 style='text-align: center;'>🗨️ Hello</h1>", unsafe_allow_html=True)


with st.expander("Important note on Generative AI"):
    st.write("Generative AI may produce inaccurate information about people, places, or facts. Please check your results carefully and do not regard them as trustworthy.")
    
st.markdown("<h3 style='text-align: center;'>🐶 Choose the appropriate option from the Menu on the left</h3>", unsafe_allow_html=True)
