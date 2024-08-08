import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO
from datetime import datetime


# Load .env file
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI or Azure OpenAI based on selection
def initialize_openai():
    return OpenAI(api_key=openai_api_key)
    
# Sidebar settings
def sidebar_settings():
    st.sidebar.header("Image Generation Settings")
    image_size = st.sidebar.selectbox("Image size", ["1024x1024", "1024x1792", "1792x1024"])
    quality = st.sidebar.selectbox("Image quality", ["standard", "high"])
    
    st.session_state.image_size = image_size
    st.session_state.quality = quality

def main():
    st.title("Image Generation with DALL-E 3")
    
    sidebar_settings()

    client = initialize_openai()
    prompt = st.text_input("Enter your prompt for image generation:")
    
    if st.button("Generate Image"):
        with st.spinner("Generating image..."):
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size=st.session_state.image_size,
                    quality=st.session_state.quality
                )
                st.session_state.image = response.data[0]  # Ensure this is a dictionary
            except Exception as e:
                st.error(f"Error generating image: {e}")
    
    if "image" in st.session_state:
        st.header("Generated Image")
        img_url = st.session_state.image.url
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        st.image(img, caption="Generated Image", use_column_width=True)
        
        if st.button("Save Image"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sanitized_prompt = "".join([c for c in prompt if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            filename = f"generated_images/dalle_image_{timestamp}_{sanitized_prompt}.png"
            img.save(filename)
            st.success(f"Image saved to disk as {filename}!")

if __name__ == "__main__":
    main()