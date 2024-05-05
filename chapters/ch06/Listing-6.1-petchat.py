import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2023-07-01-preview",
    api_key=os.getenv("AOAI_KEY")
)

#openai.api_version = "2023-05-15"

conversation=[{"role": "system", "content": "You are an AI assistant that helps people find information. You can only talk about pets and nothing else. If you don't know the answer, say, \"Sorry bud, I don't know that.\" And if you cannot answer it, say \"Sorry mate, can't answer that - I am not allowed to\"."}]
print("Please enter what you want to talk about:\n")

while True:
    user_input = input("> ")
    if user_input.lower() == "exit":
        break
    
    conversation.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt4-32k",
        messages=conversation)

    conversation.append({"role": "assistant", "content": response.choices[0].message.content})
    print("\nAI:" + response.choices[0].message.content + "\n")
