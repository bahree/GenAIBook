import os
import openai
import requests
import json
import datetime
import re

openai.api_type="open_ai"
openai.api_key = os.getenv("OPENAI_API_BOOK_KEY")
openai.organization = os.getenv("OPENAI_API_BOOK_ORG")

image_count = 4
image_size = "1024x1024"
orginal_image = ".\images\serene_vacation_lake_house.png"

# Set the directory where we'll store the image
image_dir = os.path.join(os.curdir, 'images')

# Make sure the directory exists
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# Function to clean up filenames
def valid_filename(s):
    s = re.sub(r'[^\w_.)( -]', '', s).strip()
    return re.sub(r'[\s]+', '_', s)

def generate_images_variations(image_path: str):                        
    response = openai.Image.create_variation(
        image=open(image_path, "rb"),
        n=image_count,
        size=image_size
    )
    return response

response = generate_images_variations(orginal_image)                                

for i, item_image in enumerate(response['data']):
    image = requests.get(item_image['url']).content
    filename = f"{valid_filename(os.path.basename(orginal_image))}_variation_{i+1}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    
    image_path = os.path.join(image_dir, filename)
    
    with open(image_path, "wb") as f:
        f.write(image)