# Listing: 3.1 - List the models available in Azure OpenAI
import os
import openai

openai.api_type = "azure"
openai.api_base = os.getenv("AOAI_ENDPOINT")
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AOAI_KEY")

# Call the models API to retrieve a list of available models
models = openai.Model.list()

# save to file
with open('azure-oai-models.json', 'w') as file:
    file.write(str(models))
    
# Print out the names of all the available models, and their capabilities
for model in models['data']:
    print("ID:", model['id'])
    print("Current status:", model['lifecycle_status'])
    print("Model capabilities:", model['capabilities'])
    print("-------------------")
