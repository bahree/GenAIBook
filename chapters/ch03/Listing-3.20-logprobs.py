import os
import openai

openai.api_type = "azure"
openai.api_base = os.getenv("AOAI_ENDPOINT")
openai.api_version = "2022-12-01"
openai.api_key = os.getenv("AOAI_KEY")

prompt_startphrase = "Suggest one word name for a white miniature poodle."

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Suggest a one word name for a white miniature poodle.",
  temperature=0.8,
  max_tokens=100,
  logprobs=3,
  stop=None)

responsetext = response["choices"][0]["text"]

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)

print(response)
