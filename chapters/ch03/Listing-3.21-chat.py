#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai

openai.api_type = "azure"
openai.api_base = os.getenv("AOAI_ENDPOINT")
openai.api_version = "2023-05-15"
#openai.api_version = "2023-06-01-preview"
openai.api_key = os.getenv("AOAI_KEY")

print(openai.api_base)
print(openai.api_key)

response = openai.ChatCompletion.create(
  engine="turbo", # engine = "deployment_name".
  messages = [
      {"role":"system","content":"You are an AI assistant that helps people find information."},
      {"role":"user","content":"Hello world"},
      {"role":"assistant","content":"Hello! How can I assist you today?"},
      {"role":"user","content":"I want to know more about pets and why dogs are good for humans?"}],
  temperature=0.8,
  max_tokens=800,
  user="amit",
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)

print(response)
print(response['choices'][0]['message']['content'])
