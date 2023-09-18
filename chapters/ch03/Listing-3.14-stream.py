import os
import sys
import openai

openai.api_type = "azure"
openai.api_base = os.getenv("AOAI_ENDPOINT")
openai.api_version = "2022-12-01"
openai.api_key = os.getenv("AOAI_KEY")

prompt_startphrase = "Suggest three names for a new pet salon business. The generated name ideas should evoke positive emotions and the following key features: Professional, friendly, Personalized Service."

for response in openai.Completion.create(
  engine="text-davinci-003",
  prompt=prompt_startphrase,
  temperature=0.8,
  max_tokens=500,
  n=1,
  stream=True,
  stop=None):
    for choice in response.choices:
        #sys.stdout.write(choice.text)
        sys.stdout.write(str(choice)+"\n")
        sys.stdout.flush()
    