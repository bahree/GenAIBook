import base64
import os
import requests
import datetime
import re

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = "https://api.stability.ai"

# write a python function that takes a prompt and uses stability AI to generate a image and save it to a file
def generate(prompt):
    # encode prompt to base64
    prompt = base64.b64encode(prompt.encode("utf-8")).decode("utf-8")

    # get the response from the API
    response = requests.post(f"{api_host}/v1/engines/{engine_id}/completions", json={"prompt": prompt})

    # get the image from the response
    image = response.json()["choices"][0]["text"]

    # decode the image from base64
    image = base64.b64decode(image)

    # save the image to a file
    with open(f"images/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png", "wb") as file:
        file.write(image)

