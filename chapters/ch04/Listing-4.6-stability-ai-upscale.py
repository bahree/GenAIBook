import base64
import os
import requests
import datetime
import re


engine_id = "esrgan-v1-x2plus"
api_host = "https://api.stability.ai"
api_key = os.getenv("STABILITY_API_KEY")

orginal_image = "images/serene_vacation_lake_house.jpg"

# Set the directory where we'll store the image
image_dir = os.path.join(os.curdir, 'images')

# Make sure the directory exists
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# Function to clean up filenames
def valid_filename(s):
    s = re.sub(r'[^\w_.)( -]', '', s).strip()
    return re.sub(r'[\s]+', '_', s)

if api_key is None:
    raise Exception("Missing Stability API key.")

response = requests.post(
    f"{api_host}/v1/generation/{engine_id}/image-to-image/upscale",
    headers={
        "Accept": "image/png",
        "Authorization": f"Bearer {api_key}"
    },
    files={
        "image": open(orginal_image, "rb")
    },
    data={
        "width": 2048,
    }
)

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

filename = f"{valid_filename(os.path.basename(orginal_image))}_upscale_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
image_path = os.path.join(image_dir, filename)

with open(image_path, "wb") as f:
    f.write(response.content)
