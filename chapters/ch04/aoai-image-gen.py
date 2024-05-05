import os
import openai
import requests
import json
import datetime
import re

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_BOOK_KEY"))

# Set the prompt and other parameters
image_count = 1
image_size = "1024x1024"
prompt = "a pineapple that's made of rainbow cake inside, food photography style"

# Set the directory where we'll store the image
image_dir = os.path.join(os.curdir, 'images')

# Make sure the directory exists
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# Function to clean up filenames
def valid_filename(s):
    s = re.sub(r'[^\w_.)( -]', '', s).strip()
    return re.sub(r'[\s]+', '_', s)

# Function to save the image
def save_image(image_url: str):
    image_response = requests.get(image_url)
    filename = f"{valid_filename(prompt)}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image_path = os.path.join(image_dir, filename)
    
    with open(image_path, "wb") as f:
        f.write(image_response.content)

# Function to generate the image 
def generate_images(prompt_startphrase: str):
    response = client.images.generate(
        prompt=prompt_startphrase,
        n=image_count,
        model="dall-e-3",
        style="natural",
        quality="standard",
        size=image_size)
    return response

# Save the image
response = generate_images(prompt)
image_url = response.data[0].url
save_image(image_url)                                               