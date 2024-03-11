#debugging
import os
import re
import textwrap
from time import sleep
from openai import AzureOpenAI
from tqdm import tqdm # for progress bars
import tiktoken as tk
import nltk

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AOAI_KEY"),
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2022-12-01")

# load a text file that you want to chunk
TEXT_FILE = "./data/women_fifa_worldcup_2023.txt"

# function that splits the text into chunks based on sentences
def split_sentences(text):
    sentences = re.split('[.!?]', text)
    sentences = [sentence.strip() for sentence in sentences if sentence]
    return sentences

# function that splits the text into chunks based on sentences
def split_sentences_by_textwrap(text):
    # set the maximum chunk size to 2048 characters
    max_chunk_size = 2048
    # use the wrap function to split the text into chunks
    chunks = textwrap.wrap(
        text,
        width=max_chunk_size,
        break_long_words=False,
        break_on_hyphens=False)
    
    # return the list of chunks
    return chunks

# function that splits the text into chunks based on sentences
def split_sentences_by_nltk(text):
  chunks = []

  for sentence in nltk.sent_tokenize(text):
    #num_tokens_in_sentence = len(nltk.word_tokenize(sentence))
    #print(sentence)
    chunks.append(sentence)

  return chunks

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

# function that generates summaries for each chunk
def generate_summaries(chunks):
    # create an empty list to store the summaries
    summaries = []
    # loop through each chunk
    for chunk in tqdm(chunks):
        # create a prompt that instructs the model to summarize the chunk
        prompt = f"Summarize the following text in one sentence:\n{chunk}\nSummary:"
        
        # use the OpenAI.Completion class to generate a summary for the chunk
        response = client.completions.create(
            model="dv3",
            prompt=prompt,
            max_tokens=800,
            temperature=0.7)
        
        # get the summary from the response
        summary = response.choices[0].text
        
        # append the summary to the list of summaries
        summaries.append(summary)
        
        sleep(1) # sleep for 3 seconds for rate limiting

    # return the list of summaries
    return summaries

def main():
    # read the text from the file
    with open(TEXT_FILE, "r") as f:
        text = f.read()

    print("Starting simple sentence chunking ...")
    sentences = split_sentences(text)
    print("Number of sentences:", len(sentences))
    
    # Initialize an empty 2D array
    sentence_embeddings = []
    total_token_count = 0

    for sentence in tqdm(sentences):    
        # Count the number of tokens in the sentence
        total_token_count += count_tokens(sentence, "cl100k_base")
        
        # Append the sentence and its embedding to the 2D array
        embedding = get_embedding(sentence)
        sentence_embeddings.append([sentence, embedding])
        
    print("Simple Sentence Chunking:")
    print("\tNumber of sentence embeddings:", len(sentence_embeddings))
    print("\tTotal number of tokens:", total_token_count)

    print("="*20)
    # ===================================

    #Reset variables
    summaries = []
    sentences = []
    sentence_embeddings = []
    total_token_count = 0
    chunks = []

    print("2. Starting sentence chunking using textwrap ...")
    # split the text into chunks by sentences
    chunks = split_sentences_by_textwrap(text)
    print(f"Number of chunks: {len(chunks)}")

    for sentence in tqdm(chunks):
        # Count the number of tokens in the sentence
        total_token_count += count_tokens(sentence, "cl100k_base")
        
        # Append the sentence and its embedding to the 2D array
        embedding = get_embedding(sentence)
        sentence_embeddings.append([sentence, embedding])

    # Now, sentence_embeddings is a 2D array where each element is a list of the form [sentence, embedding]
    print("Sentence chunking using textwrap:")
    print("\tNumber of sentence embeddings:", len(sentence_embeddings))
    print("\tTotal number of tokens:", total_token_count)
    
    print("="*20)
    # ===================================

    #Reset variables
    summaries = []
    sentences = []
    sentence_embeddings = []
    total_token_count = 0
    chunks = []

    print("3. Starting sentence chunking using NLTK ...")
    # split the text into chunks by sentences
    chunks = split_sentences_by_nltk(text)
    print(f"Number of chunks: {len(chunks)}")

    for sentence in tqdm(chunks):
        # Count the number of tokens in the sentence
        total_token_count += count_tokens(sentence, "cl100k_base")
        
        # Append the sentence and its embedding to the 2D array
        embedding = get_embedding(sentence)
        sentence_embeddings.append([sentence, embedding])

    # Now, sentence_embeddings is a 2D array where each element is a list of the form [sentence, embedding]
    print("Sentence chunking using NLTK:")
    print("\tNumber of sentence embeddings:", len(sentence_embeddings))
    print("\tTotal number of tokens:", total_token_count)

    # generate summaries for each chunk using OpenAI API
    summaries = generate_summaries(chunks)

    # print the summaries
    print(summaries)
    
if __name__ == "__main__":
    main()