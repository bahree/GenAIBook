import os
from openai import OpenAI
import tiktoken as tk

# Set your OpenAI API key
API_KEY = os.getenv("OPENAI_API_BOOK_KEY")
MODEL = "gpt-4o"
DEBUG = True
TEMPERATURE = 0.95
MAX_TOKENS = 1000


client = OpenAI(api_key=API_KEY)

def list_models(client):
    # Call the models API to retrieve a list of available models
    models = client.models.list()

    if DEBUG:
        print(models)

    # Print out the organization that owns the models
    for model in models.data:
        print("ID:", model.id)
        print("Model owned by:", model.owned_by)
        print("-------------------")

# Generate a story about a topic using the chat endpoint
def generate_story(client, topic):
    response = client.chat.completions.create(
        model=MODEL,
        messages = [{"role": "system", "content": "Once upon a time, there was a story about " + topic}],
        temperature = TEMPERATURE,
        max_tokens = MAX_TOKENS
    )
    generation = response.choices[0].message.content
    if DEBUG:
        print("Tokens:", count_tokens(generation, MODEL))
        
    return generation

def count_tokens(string: str, model_name: str) -> int:
    # Get the encoding
    encoding = tk.get_encoding("cl100k_base")
    
    # Encode the string
    encoded_string = encoding.encode(string, disallowed_special=())

    # Count the number of tokens
    num_tokens = len(encoded_string)
    return num_tokens

if __name__ == "__main__":
    print(generate_story(client, "interesting facts about Seattle"))
