import os
import re
from time import sleep
import time
import textwrap
from openai import AzureOpenAI
from tqdm import tqdm # for progress bars
import tiktoken as tk
import nltk
import spacy

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AOAI_KEY"),
    azure_endpoint=os.getenv("AOAI_ENDPOINT"),
    api_version="2024-05-01-preview")

GPT_MODEL = "gpt-35-turbo"

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

def split_sentences_by_nltk(text):
  chunks = []

  for sentence in nltk.sent_tokenize(text):
    #num_tokens_in_sentence = len(nltk.word_tokenize(sentence))
    #print(sentence)
    chunks.append(sentence)
    
  return chunks

def split_sentences_by_spacy(text, max_tokens, 
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
    response = client.embeddings.create(model="ada-embedding",
    input=text)
    return response.data[0].embedding

def generate_summaries(chunks):
    # create an empty list to store the summaries
    summaries = []
    
    # loop through each chunk
    for chunk in tqdm(chunks):
        # create a prompt that instructs the model to summarize the chunk
        prompt = f"Summarize the following text in one sentence:\n{chunk}\nSummary:"
        
        # use the OpenAI.Completion class to generate a summary for the chunk
        response = client.completions.create(
            model=GPT_MODEL,
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7)
        
        # get the summary from the response
        #summary = response["choices"][0]["text"]
        summary = response.choices[0].text
        # append the summary to the list of summaries
        summaries.append(summary)
        sleep(1) # sleep for 1 second(s) for rate limiting

    # return the list of summaries
    return summaries

def process_chunks(sentences):
    sentence_embeddings = []
    total_token_count = 0

    for sentence in tqdm(sentences):
        # Count the number of tokens in the sentence
        total_token_count += count_tokens(sentence, "cl100k_base")
        
        # Append the sentence and its embedding to the 2D array
        embedding = get_embedding(sentence)
        sentence_embeddings.append([sentence, embedding])

    #print("Simple Sentence Chunking:")
    print("\tNumber of sentence embeddings:", len(sentence_embeddings))
    print("\tTotal number of tokens:", total_token_count)

    return sentence_embeddings

def main():
    # load a text file that you want to chunk
    TEXT_FILE = "./data/women_fifa_worldcup_2023.txt"
    
    print("Reading the file ...")
    
    # read the text from the file
    with open(TEXT_FILE, "r") as f:
        text = f.read()

    print("1. Simple sentence chunking ...")
    start_time = time.time()
    sentences = split_sentences(text)

    #print("Number of sentences:", len(sentences))
    process_chunks(sentences)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")

    print("="*20)
    # ===================================

    #Reset variables
    summaries = []
    sentences = []
    sentence_embeddings = []
    total_token_count = 0
    chunks = []

    print("2. Sentence chunking using textwrap ...")
    start_time = time.time()
    # split the text into chunks by sentences
    chunks = split_sentences_by_textwrap(text)
    #print(f"Number of chunks: {len(chunks)}")
    process_chunks(chunks)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")


    print("="*20)
    # ===================================

    #Reset variables
    summaries = []
    sentences = []
    chunks = []

    print("3. Sentence chunking using NLTK ...")
    # split the text into chunks by sentences
    chunks = split_sentences_by_nltk(text)
    #print(f"Number of chunks: {len(chunks)}")
    start_time = time.time()
    process_chunks(chunks)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")

    print("="*20)
    # ===================================

    #Reset variables
    summaries = []
    sentences = []
    chunks = []

    print("4. Sentence chunking using spaCy ...")
    # split the text into chunks by sentences
    start_time = time.time()
    chunks = split_sentences_by_spacy(text, max_tokens=2000, overlap=0)
    #print(f"Number of chunks: {len(chunks)}")
    process_chunks(chunks)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")

    print("="*20)
    # ===================================
    # generate summaries for each chunk using OpenAI API
    summaries = generate_summaries(chunks)
    print("Summaries generated by OpenAI API:")
    # print the summaries
    print(summaries)

if __name__ == "__main__":
    main()