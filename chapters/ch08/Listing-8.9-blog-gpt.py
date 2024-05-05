import numpy as np
from redis.commands.search.query import Query
import redis
import os
from openai import OpenAI
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
import tiktoken as tk

# OpenAI API key
client = OpenAI(api_key=os.getenv('OPENAI_API_BOOK_KEY'))

# Redis connection details
# redis_host = os.getenv('REDIS_HOST')
# redis_port = os.getenv('REDIS_PORT')
# redis_password = os.getenv('REDIS_PASSWORD')
redis_host = "localhost"
redis_port = "6379"
redis_password = ""

# Count the number of tokens in a string
def count_tokens(string: str, encoding_name="cl100k_base") -> int:
    # Get the encoding
    encoding = tk.get_encoding(encoding_name)
    
    # Encode the string
    encoded_string = encoding.encode(string, disallowed_special=())

    # Count the number of tokens
    num_tokens = len(encoded_string)
    return num_tokens

# Vectorize the query using OpenAI's text-embedding-ada-002 model
def get_embedding(text):
    # vectorize with OpenAI text-emebdding-ada-002
    embedding = client.embeddings.create(input=text,
    model="text-embedding-ada-002")

    vector = embedding.data[0].embedding
    
    return vector

# Perform a hybrid search using Redis search and return the top-k results
def hybrid_search(query_vector, client, top_k=5, hybrid_fields="*"):
    base_query = f"{hybrid_fields}=>[KNN {top_k} @embedding $vector AS vector_score]"
    query = Query(base_query).return_fields("url", 
                                            "title",
                                             "publish_date",
                                             "description",
                                             "content",
                                             "vector_score").sort_by("vector_score").dialect(2)

    try:
        results = client.ft("posts").search(query, query_params={"vector": query_vector})
    except Exception as e:
        print("Error calling Redis search: ", e)
        return None
    
    if results.total == 0:
        print("No results found for the given query vector.")
        return None
    elif results.total < top_k:
        print(f"Only {results.total} results found for the given query vector.")

    return results

# Return a message for GPT, with relevant source texts pulled from a the vector db.
def get_search_results(query: str, max_token = 4096, debug_message=False) -> str:
    # Connect to the Redis server
    conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, encoding='utf-8', decode_responses=True)

    if conn.ping():
        if debug_message:
            print("Connected to Redis")

    # Vectorize the query using OpenAI's text-embedding-ada-002 model
    query_vector = get_embedding(query)

    # Convert the vector to a numpy array
    query_vector = np.array(query_vector).astype(np.float32).tobytes()

    # Perform the similarity search
    print("Searching for similar posts...")
    results = hybrid_search(query_vector, conn, top_k=5)
    
    # We reduce the token budget by 2000 to account for the query and the prompt.
    token_budget = max_token - count_tokens(query) - 2000
    if debug_message:
        print(f"Token budget: {token_budget}")

    message = 'Use the blog post below to answer the subsequent question. \
            If the answer cannot be found in the articles, write \
            "Sorry, I could not find an answer in the blog posts."'
    
    question = f"\n\nQuestion: {query}"

    if results:
        for i, post in enumerate(results.docs):
            next_post = f'\n\nBlog post:\n"""\n{post.content}\n"""'
            new_token_usage = count_tokens(message + question + next_post)
            if new_token_usage < token_budget:
                if debug_message:
                    print(f"Token usage: {new_token_usage}")
                message += next_post
            else:
                break
    else:
        print("No results found")

    return message + question

# Ask GPT a question based on the search results
def ask_gpt(query : str, max_token = 4096, debug_message = False) -> str:
    message = get_search_results(
        query,
        max_token,
        debug_message=debug_message)
    
    if debug_message:
        print(message)
    
    # Ask GPT
    messages = [ 
        {"role": "system", 
         "content": "You answer questions in summary from the blog posts."},
        {"role": "user",
            "content": message},]
    
    if debug_message:
        print("Length of messages: ", len(messages))
        if debug_message:
            print("Total tokens: ", count_tokens(messages))
            print(messages)

    response = client.chat.completions.create(
        #engine=model,
        # #model="gpt-4",
        model="gpt-3.5-turbo-16k",
        messages=messages,
        temperature=0.5,
        max_tokens=2000,
        top_p=0.95)
    
    response_message = response.choices[0].message.content
    
    return response_message

# Main function
if __name__ == "__main__":
    # Enter a query
    while True:
        query = input("Please enter your query: ")
        print(ask_gpt(query, max_token=15000, debug_message=False))
        print("=="*20)
