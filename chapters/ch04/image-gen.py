import requests
import json
import os
import openai
import datetime

# function to read the key
def read_api_key(file_path: str) -> str:
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

# Download and save image
def save_image(image_url: str):
    image_response = requests.get(image_url)
    filename = f"dalle_image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    with open(filename, "wb") as f:
        f.write(image_response.content)

# Setup the OpenAI API key and organization
api_key_file = 'OPENAI_API_BOOK_KEY.key'
openai.organization = "org-rocrupyvzgcl4yf25rqq6d1v"
api_key = read_api_key(api_key_file)

# API endpoint URL
url = "https://api.openai.com/v1/images/generations"

# Prompt text
#prompt = "a angry panda eating bamboo sitting in a car driving on the beach"
#prompt = "Cover Picture of a book on generative AI for developers that shows a human entering a prompt and getting a generated image."
#prompt = "Cover of a book on generative AI for enterprise developers"
#prompt = "A panda eating a krispy kreme donut sitting next to a window while it is raining outside."
#prompt = "Generate an image of a dog wearing glasses sitting at a table and authoring a book on AI using a computer. Make it a positive image with the background of the taj mahal in the window in the distance at the golden hour."
prompt = "laughing panda"

# Request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Request body
data = {
    # "model": "image-alpha-001",
    "prompt": prompt,
    "num_images": 2,
    "size": "1024x1024"
}

# Make API request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Parse response JSON
response_data = response.json()
image_url = response_data["data"][0]["url"]
#print(image_url)
print(response_data)
