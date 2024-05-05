# Listing: 3.1 - List the models available in Azure OpenAI
import os
from openai import AzureOpenAI
import json

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2023-05-15",
    api_key=os.getenv("AOAI_KEY")
    )

# Call the models API to retrieve a list of available models
models = client.models.list()

# save to file
# Convert each Model object in models to a dictionary before serializing it to JSON.
with open('azure-oai-models.json', 'w') as file:
    models_dict = [model.__dict__ for model in models]
    json.dump(models_dict, file)
    
# Print out the names of all the available models, and their capabilities
for model in models:
    print("ID:", model.id)
    print("Current status:", model.lifecycle_status)
    print("Model capabilities:", model.capabilities)
    print("-------------------")