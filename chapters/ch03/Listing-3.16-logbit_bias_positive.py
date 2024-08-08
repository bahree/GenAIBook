import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

# This model name is what you chose when you deployed the model in Azure OpenAI
GPT_MODEL = "gpt-35-turbo"
  
prompt_startphrase = "Suggest three names for a new pet salon business. The generated name ideas should evoke positive emotions and the following key features: Professional, friendly, Personalized Service."

response = client.completions.create(
    model=GPT_MODEL,
    prompt=prompt_startphrase,
    temperature=0.8,
    max_tokens=100,
    logit_bias={
        30026:-100,
        81:-100,
        9330:-100,
        808:-100,
        42114:-100,
        1308:-100, 
        3808:-100,
        502:-100,
        322:-100,
        37:5,
        16682:5
    }
)
  
responsetext = response.choices[0].text
print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)
