import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview",
    api_key=os.getenv("AOAI_KEY"))

GPT_MODEL = "gpt-35-turbo"

conversation=[{"role": "system", "content": "You are a helpful AI assistant and happy to talk about pets and salons."}]

while True:
    user_input = input()      
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=conversation
    )

    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    print("\n" + response.choices[0].message.content + "\n")