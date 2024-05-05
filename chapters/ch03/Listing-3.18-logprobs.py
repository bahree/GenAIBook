import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2022-12-01",
    api_key=os.getenv("AOAI_KEY"))

# This model name is what you chose when you deployed the model in Azure OpenAI
GPT_MODEL = "text-davinci-003"

prompt_startphrase = "Suggest one word name for a white miniature poodle."

response = client.completions.create(
    model=GPT_MODEL,
    prompt="Suggest a one word name for a white miniature poodle.",
    temperature=0.8,max_tokens=100,
    logprobs=3,
    stop=None)

responsetext = response.choices[0].text

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)
