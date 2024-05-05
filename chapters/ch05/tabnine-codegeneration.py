import base64
import os
import requests
import datetime
import re

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = "https://api.stability.ai"
api_key = os.getenv("STABILITY_API_KEY")

# write a python function that takes a prompt and uses stability AI to generate a image and save to a file
def generate_image(prompt):
    url = f"{api_host}/v1/engines/{engine_id}/generate?prompt={prompt}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code!= 200:
        print(f"Error: {response.status_code}")
    else:
        print(f"Prompt: {prompt}")

    image = response.json()["image"]
    with open(f"{prompt}.png", "wb") as f:
        