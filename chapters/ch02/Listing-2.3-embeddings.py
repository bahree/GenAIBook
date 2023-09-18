import openai

def get_embedding(text):
    response = openai.Embedding.create(
      engine="text-embedding-ada-002",
      input=text,
    )
    return response['data'][0]['embedding']

embeddings = get_embedding("I have a white dog named Champ.")
print(embeddings)