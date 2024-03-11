# Use spaCy to tokenize the text into sentences.
# Use tiktoken to count the tokens accurately.
# Slide through the sentences using a window (defined by the token limit), optionally allowing overlaps.

# pip install spacy
# python -m spacy download en_core_web_sm

import spacy
import tiktoken as tk
from openai import AzureOpenAI
import os

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AOAI_KEY"),
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2022-12-01")

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
        model="ada-embedding",
        input=text)
    
    return response.data[0].embedding

# function that splits the text into chunks based on sentences
def chunking_with_spacy(text, max_tokens, 
                        overlap=0, 
                        model="en_core_web_sm"):
    # Load spaCy model
    nlp = spacy.load(model)
    
    # Tokenize the text into sentences using spaCy
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    
    # Tokenize sentences into tokens and accumulate tokens
    tokens_lengths = [count_tokens(sent) for sent in sentences]
    
    chunks = []
    start_idx = 0
    
    while start_idx < len(sentences):
        current_chunk = []
        current_token_count = 0
        for idx in range(start_idx, len(sentences)):
            if current_token_count + tokens_lengths[idx] > max_tokens:
                break
            current_chunk.append(sentences[idx])
            current_token_count += tokens_lengths[idx]
        
        chunks.append(" ".join(current_chunk))
        
        # Sliding window adjustment
        if overlap >= len(current_chunk):
            start_idx += 1
        else:
            start_idx += len(current_chunk) - overlap

    return chunks

if __name__ == "__main__":
    # Example
    text = ("This is a demonstration of text chunking with spaCy and tiktoken. "
        "Using both allows for precise token counting and effective chunking. "
        "Overlap and sliding window strategies are useful for various applications. "
        "Choose your strategy based on your requirements.")

    max_tokens = 25
    overlap_sentences = 2
    chunks = chunking_with_spacy(text, max_tokens, overlap=overlap_sentences)

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:\n{chunk}\n")
