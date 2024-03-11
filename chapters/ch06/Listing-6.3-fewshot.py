import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2022-12-01",
    api_key=os.getenv("AOAI_KEY")
)

prompt_startphrase = "Definition: A \"whatpu\" is a small, furry animal native to Tanzania. \nExample: We were traveling in Africa and we saw these very cute whatpus.\n\nDefinition: To do a \"farduddle\" means to jump up and down really fast. \nExample: One day when I was playing tag with my little sister, she got really excited and she started doing these crazy farduddles.\n\nDefinition: A \"yalubalu\" is a type of vegetable that looks like a big pumpkin. \nExample:"

response = client.completions.create(
    model="dv3",
    prompt=prompt_startphrase,
    temperature=0.8,
    max_tokens=100,
    stop=None)

responsetext = response.choices[0].text

print("Prompt:" + prompt_startphrase + "\nResponse:" + responsetext)
