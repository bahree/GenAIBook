import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text)
    return response.data[0].embedding

embeddings = get_embedding("I have a white dog named Champ.")
print("Embedding Length:", len(embeddings))
print("Embedding:", embeddings[:5])
