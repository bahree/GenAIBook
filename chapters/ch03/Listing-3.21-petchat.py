import os
import openai

openai.api_type = "azure"
openai.api_base = os.getenv("AOAI_ENDPOINT")
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AOAI_KEY")

conversation=[{"role": "system", "content": "You are a helpful AI assistant and happt to talk about pets and salons."}]

while True:
    user_input = input()      
    conversation.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        engine="turbo", 
        messages=conversation
    )

    conversation.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
    print("\n" + response['choices'][0]['message']['content'] + "\n")