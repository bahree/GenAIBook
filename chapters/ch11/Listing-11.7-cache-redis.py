# pip install redisvl

# Check if it is running
# look at the index specification created for the semantic cache lookup
# !rvl index info -i llmcache

import os
import time
from openai import AzureOpenAI
from redisvl.extensions.llmcache import SemanticCache
import numpy as np
import random

# Set your OpenAI API key
AOAI_API_KEY = os.getenv("AOAI_KEY")
AZURE_ENDPOINT = os.getenv("AOAI_ENDPOINT")
API_VERSION = "2024-02-15-preview"

MODEL = "gp4"
TEMPERATURE = 0.75
TOP_P = 0.95
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0
MAX_TOKENS = 25
DEBUG = True

def initialize_cache():
    # Initialize the semantic cache
    llmcache = SemanticCache(
        name="GenAIBookCache",                # Index name
        prefix="bookcache",                   # redis key-prefix for hash entries
        redis_url="redis://localhost:6379",   # redis connection url string
        distance_threshold=0.1                # semantic cache distance threshold
    )
    return llmcache

# Initialize OpenAI client
client = AzureOpenAI(
  azure_endpoint = AZURE_ENDPOINT, 
  api_key=AOAI_API_KEY,  
  api_version=API_VERSION
)

# Define a list of questions
input_questions = ["What is the capital of UK?",
                   "What is the capital of France?",
                   "What's the square root of 144?",
                   "What is the capital of WA state?",
                   "What is the capital of USA?",
                   "What is the capital of Canada?",
                   "What is the capital of Australia?",
                   "What is the capital of India?",
                   "What is the capital of China?",
                   "What is the capital of Japan?"]

# Generate response using OpenAI API
def generate_response(conversation, max_tokens=25)->str:
    response = client.chat.completions.create(
        model=MODEL,
        messages = conversation,
        temperature = TEMPERATURE,
        max_tokens = max_tokens,
    )
    return response.choices[0].message.content

# Function to answer a question using the cache
def answer_question(question: str) -> str:
    conversation = [{"role": "assistant", "content": question}]
    
    results = llmcache.check(prompt=question)
    if results:
        answer = results[0]["response"]
        if DEBUG:
            print(f"Cache hit for prompt: {question}, answer: {answer}")
    else:
        answer = generate_response(conversation)
        llmcache.store(prompt=question, response=answer)
        if DEBUG:
            print(f"Cache miss for prompt: {question}, added to cache with response: {answer}")
    
    return answer

if __name__ == "__main__":
    llmcache = initialize_cache()

    times_without_cache = []
    times_with_cache = []

    for question in input_questions:
        # Without caching
        start_time = time.time()
        answer = generate_response([{"role": "assistant", "content": question}])
        end_time = time.time()
        times_without_cache.append(end_time-start_time)

        # With caching
        start_time = time.time()
        answer = answer_question(question)
        end_time = time.time()
        times_with_cache.append(end_time-start_time)

    avg_time_without_cache = np.mean(times_without_cache)
    avg_time_with_cache = np.mean(times_with_cache)

    print(f"Avg time taken without cache: {avg_time_without_cache}")
    print(f"Avg time taken with LLM cache enabled: {avg_time_with_cache}")
    print(f"Percentage of time saved: {round((avg_time_without_cache - avg_time_with_cache) / avg_time_without_cache * 100, 2)}%")