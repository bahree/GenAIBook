import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint="https://demoinstance.openai.azure.com/",
    api_version="2023-09-15-preview",
    api_key="enter-your-key")

prompt_startphrase = "Suggest three names for a new pet salon business. The generated name ideas should evoke positive emotions and the following key features: Professional, friendly, Personalized Service."

response = client.completions.create(
    model="gpt-turbo-35",
    prompt=prompt_startphrase,
    temperature=0.7,
    max_tokens=100,
    stop=None)

responsetext = response.choices[0].text

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)
