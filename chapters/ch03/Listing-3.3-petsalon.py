import os
import openai

openai.api_type = "azure"
openai.api_base = os.getenv("AOAI_ENDPOINT")
openai.api_version = "2022-12-01"
openai.api_key = os.getenv("AOAI_KEY")

prompt_startphrase = "Suggest three names for a new pet salon business."

response = openai.Completion.create(
  engine="text-davinci-003",
  prompt=prompt_startphrase,
  temperature=0.8,
  max_tokens=100,
  suffix="\nThats all folks!",
  stop=None)

responsetext = response["choices"][0]["text"]

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)

print(response)

