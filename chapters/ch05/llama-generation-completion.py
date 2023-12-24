# write a python function that takes a prompt and uses stability AI to generate a image and save it to a file
# the function should return the path of the saved image

import os
import sys
import time
from PIL import Image
import numpy as np
import torch
import torch.nn.functional as F
import clip
from tqdm import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_image(prompt):
    with torch.no_grad():
        text = clip.tokenize([prompt]).to(device)
        image = model.encode_image(preprocess(Image.open("./images/0.jpg"))).float()
        text = text.repeat(image.shape[0], 1).to(device)
        logits_per_image, logits_per_text = model(image, text)
        probs = F.softmax(logits_per_image, dim=-1)
        probs, ids = probs.sort(dim=-1, descending=True)
        probs = probs[:, :5]
        ids = ids[:, :5]
        index = torch.arange(ids.shape[0])[:, None].repeat(1, 5)
        ids = ids[index, torch.arange(5)]
        ids = ids.cpu().numpy()
        probs = probs.cpu().numpy()
        for i in range(len(ids)):
            for j in range(5):
                print(f"{clip.tokenize([prompt])[0]} {probs[i][j]:.4f} {ids[i][j]}")
        return ids[0][0]

def generate_image(prompt):
    image_id = get_image(prompt)
    image = Image.open(f"./images/{image_id}.jpg").convert("RGB")
    image.save(f"./generated/{prompt}.png")
    return f"./generated/{prompt}.png"

if __name__ == "__main__":
    if not os.path.exists("./generated"):
        os.mkdir("./generated")
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        generate_image(prompt)
    else:
        while True:
            prompt = input("Enter a prompt: ")
            generate_image(prompt)
            print(f"Saved to ./generated/{prompt}.png")
            print("Press enter to continue or type 'exit' to exit")
            if input() == "exit":
                break