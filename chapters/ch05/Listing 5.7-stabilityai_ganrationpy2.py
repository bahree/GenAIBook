# write a python function that takes a prompt and uses stability AI 
# to generate a image and save it to a file
def generate_image(prompt):
    if api_key is None:
        raise Exception("Missing Stability API key.")

    # Set the directory where we'll store the image
    image_dir = os.path.join(os.curdir, 'images')

    # Make sure the directory exists
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # Function to clean up filenames
    def valid_filename(s):
        s = re.sub(r'[^\w_.)( -]', '', s).strip()
        return re.sub(r'[\s]+', '_', s)

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [{ "text": f"{prompt}", "weight": 1.0}],
            "cfg_scale": 7, "height": 1024, "width": 1024,
            "samples": 1, "steps": 50,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    for i, image in enumerate(data["artifacts"]):
        filename = f"sd_{valid_filename(prompt)}_{i}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image_path = os.path.join(image_dir, filename)
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(image["base64"]))

