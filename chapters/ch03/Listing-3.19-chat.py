import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2023-05-15",
    api_key=os.getenv("AOAI_KEY"))

# This model name is what you chose when you deployed the model in Azure OpenAI
GPT_MODEL = "gpt35"

response = client.chat.completions.create(
    model=GPT_MODEL,
    messages = [
        {"role":"system","content":"You are an AI assistant that helps people find information."},
        {"role":"user","content":"Hello world"},
        {"role":"assistant","content":"Hello! How can I assist you today?"},
        {"role":"user","content":"I want to know more about pets and why dogs are good for humans?"}],
    temperature=0.8,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
)

print(response.choices[0].message.content)
