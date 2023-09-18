import os
import openai
import requests
import json
import datetime
import re

openai.api_type="open_ai"                                   #A
openai.api_key = os.getenv("OPENAI_API_BOOK_KEY")           #A
openai.organization = os.getenv("OPENAI_API_BOOK_ORG")      #A

image_count = 1                                             #B
image_size = "1024x1024"                                    #B
#prompt = "Laughing panda in the clouds eating bamboo"       #B
prompt = "a pineapple that's made of rainbow cake inside, food photography style"

# Set the directory where we'll store the image
image_dir = os.path.join(os.curdir, 'images')

# Make sure the directory exists
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# Function to clean up filenames
def valid_filename(s):                                      #C
    s = re.sub(r'[^\w_.)( -]', '', s).strip()
    return re.sub(r'[\s]+', '_', s)

def save_image(image_url: str):                             #D
    image_response = requests.get(image_url)
    filename = f"{valid_filename(prompt)}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    image_path = os.path.join(image_dir, filename)
    
    with open(image_path, "wb") as f:
        f.write(image_response.content)
            
def generate_images(prompt_startphrase: str):                        #E
    response = openai.Image.create(
        prompt=prompt_startphrase,
        n=image_count,
        size=image_size
    )
    return response

response = generate_images(prompt)                                  #F
image_url = response['data'][0]['url']                              #G
save_image(image_url)                                               
