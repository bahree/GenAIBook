
import base64
import os
import datetime
import re

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = "https://api.stability.ai"

# write a python function that takes a prompt and uses stability AI to generate a image and save it to a file

def generate(prompt : str)
    # generate image
    response = requests.post(
        f"{api_host}/v1/engines/{engine_id}/generate",
        json={
            "prompt": prompt,
            "num_inference_steps": 50,
            "strength": 0.8,
            "temperature": 0.9,
            "seed": 0,
        },
    )
    # decode image
    image_data = base64.b64decode(response.json()["image"])
    # save image
    filename = f"{prompt.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
    with open(filename, "wb") as file:
        file.write(image_data)
    return filename


    