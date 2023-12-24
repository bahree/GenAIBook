# Variant of Listing 3.1 - list models available in OpenAI for the current organization

import os
import openai
from openai import OpenAI

api_key_file = '../../OPENAI_API_BOOK_KEY.key'

# function to read the key
def read_api_key(file_path: str) -> str:
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

client = OpenAI(api_key=read_api_key(api_key_file))

# Call the models API to retrieve a list of available models
models = client.models.list()

# debug output - show response
# print(models)

# save to file
with open('oai-models.json', 'w') as file:
    file.write(str(models))

# Print out the organization that owns the models
for model in models.data:
    print("ID:", model.id)
    print("Model owned by:", model.owned_by)
    print("-------------------")