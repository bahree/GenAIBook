import feedparser
import os
import numpy as np
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
import re
from redis.commands.search.field import TagField
from tenacity import retry
from tenacity import wait_random_exponential
from time import sleep
from tqdm import tqdm
import tiktoken as tk

import spacy

# Redis connection details
# redis_host = os.getenv('REDIS_HOST')
# redis_port = os.getenv('REDIS_PORT')
# redis_password = os.getenv('REDIS_PASSWORD')
redis_host = "localhost"
redis_port = "6379"
redis_password = ""

# OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_BOOK_KEY"))

# Vectorize the query using OpenAI's text-embedding-ada-002 model
def get_embedding(text):
    # vectorize with OpenAI text-emebdding-ada-002
    embedding = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002")

    vector = embedding.data[0].embedding
    
    return vector

# count tokens
def count_tokens(string: str, encoding_name="cl100k_base") -> int:
    # Get the encoding
    encoding = tk.get_encoding(encoding_name)
    
    # Encode the string
    encoded_string = encoding.encode(string, disallowed_special=())

    # Count the number of tokens
    num_tokens = len(encoded_string)
    return num_tokens

# Split the text into chunks by sentences
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

# Connect to the Redis server
conn = redis.Redis(host=redis_host, 
                   port=redis_port, 
                   password=redis_password, 
                   encoding='utf-8', 
                   decode_responses=True)

SCHEMA = [
    TagField("url"),
    TextField("title"), 
    TextField("description"),
    TextField("publish_date"),
    TextField("content"),
    VectorField("embedding", "HNSW",
                {"TYPE": "FLOAT32",
                 "DIM": 1536,
                 "DISTANCE_METRIC": "COSINE"}),
]

# Check if the index exists
try:
    conn.ft("posts").info()
    # Yay the index exists, we do nothing
except Exception as e:
    print("Index does not exist, please create it and rerun this program.")
    exit(1)

# URL of the RSS feed to parse
url = "https://blog.desigeek.com/index.xml"

# Parse the RSS feed with feedparser
print("Parsing RSS feed...")
feed = feedparser.parse(url)

# get number of blog posts in feed
blog_posts = len(feed.entries)
print("Number of blog posts: ", blog_posts)

p = conn.pipeline(transaction=False)
for i, post in enumerate(feed.entries):
    # report progress
    print("Create embedding and save for entry #", i, " of ", blog_posts)

    r = requests.get(post.link)
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get the title
    try:    
        article_title = soup.find('h1', {'class': 'post-title'}).text
        article_title = article_title.replace("| Amit Bahree's (useless?) insight!", "")
    except AttributeError:
        article_title = ""
    print("\tTitle:" + article_title)
    
    # get the post description
    try:
        article_desc = soup.find('div', {'class': 'post-description'}).text
    except AttributeError as e:
        #print("Error getting description: ", e)
        article_desc = ""

    # get the publish date
    try:
        temp = soup.find('div', {'class': 'post-meta'}, {'span', 'title'}).text
        match = re.search(r"(\w+\s\d+,\s\d+)", temp)
        if match:
            publish_date = match.group(1)
    except AttributeError:
        publish_date = ""

    # get the article body
    try:
        article_body = soup.find('div', {'class': 'post-content'}).text
    except AttributeError:
        article_body = ""
    
    print("Title:" + article_title)
    print("Desc:" + article_desc)
    print("Date:" + publish_date)
    print("URL:" + post.link)
    # print("Body:" + article_body)

    article = article_body #This should be chunked up

    total_token_count = 0
    chunks = []

    # split the text into chunks by sentences
    chunks = split_sentences_by_spacy(article, max_tokens=3000, overlap=10)
    print(f"Number of chunks: {len(chunks)}")

    for j, chunk in enumerate(tqdm(chunks)):
        vector = get_embedding(chunk)
        # convert to numpy array
        vector = np.array(vector).astype(np.float32).tobytes()

        # Create a new hash with the URL and embedding
        post_hash = {
            "url": post.link,
            "title": article_title,
            "description": article_desc,
            "publish_date": publish_date,
            "content": chunk,
            "embedding": vector
        }
        
        conn.hset(name=f"post:{i}_{j}", mapping=post_hash)

p.execute()

print("Vector upload complete. 🤘")