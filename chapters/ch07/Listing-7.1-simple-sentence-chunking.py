import os
import re
from openai import OpenAI
from tqdm import tqdm # for progress bars
import tiktoken as tk

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_BOOK_KEY"))

# function that splits the text into chunks based on sentences
def split_sentences(text):
    sentences = re.split('[.!?]', text)
    sentences = [sentence.strip() for sentence in sentences if sentence]
    return sentences

# count tokens
def count_tokens(string: str, encoding_name="cl100k_base") -> int:
    # Get the encoding
    encoding = tk.get_encoding(encoding_name)
    
    # Encode the string
    encoded_string = encoding.encode(string)

    # Count the number of tokens
    num_tokens = len(encoded_string)
    return num_tokens

# OpenAI embeddings example from Chapter 2
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text)
    return response.data[0].embedding

if __name__ == "__main__":
    # Example usage:
    text = "This is the first sentence. This is the second sentence. Guess what? This is the fourth sentence."

    sentences = split_sentences(text)

    # Initialize an empty 2D array
    sentence_embeddings = []
    total_token_count = 0

    for sentence in tqdm(sentences):
        # Count the number of tokens in the sentence
        total_token_count += count_tokens(sentence, "cl100k_base")
        
        # Append the sentence and its embedding to the 2D array
        embedding = get_embedding(sentence)
        sentence_embeddings.append([sentence, embedding])

    # Now, sentence_embeddings is a 2D array where each element is a list of the form [sentence, embedding]
    print("Number of sentence embeddings:", len(sentence_embeddings))
    print("Total number of tokens:", total_token_count)