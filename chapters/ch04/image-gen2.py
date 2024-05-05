import os
import openai
import requests
import json
import datetime

openai.api_key = "sk-...."
openai.organization = "org-...."

image_count = 1
image_size = "1024x1024"
prompt = "Laughing panda"


# Set the directory where we'll store the image
image_dir = os.path.join(os.curdir, 'images')
# If the directory doesn't exist, create it
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)


# Download and save image
def save_image(image_url: str):
    image_response = requests.get(image_url)
    filename = f"dalle_image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image_path = os.path.join(image_dir, filename)
    
    with open(image_path, "wb") as f:
        f.write(image_response.content)
            
def generate_images(prompt_startphrase: str):
    response = openai.Image.create(
        prompt=prompt_startphrase,
        n=image_count,
        size=image_size
    )
    return response

response = generate_images(prompt)
image_url = response['data'][0]['url']
save_image(image_url)
