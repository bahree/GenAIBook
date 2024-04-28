import os
import numpy as np
from redis.commands.search.query import Query
import redis
from openai import OpenAI

# OpenAI API key
client = OpenAI(api_key=os.getenv('OPENAI_API_BOOK_KEY'))

# Redis connection details
# redis_host = os.getenv('REDIS_HOST')
# redis_port = os.getenv('REDIS_PORT')
# redis_password = os.getenv('REDIS_PASSWORD')
redis_host = "localhost"
redis_port = "6379"
redis_password = ""

DEBUG = False

# Perform a hybrid search using Redis search and return the top-k results
def hybrid_search(query_vector, client, top_k=3, hybrid_fields="*"):
    base_query = f"{hybrid_fields}=>[KNN {top_k} @embedding $vector AS vector_score]"
    query = Query(base_query).return_fields(
        "url",
        "title",
        "publish_date",
        "description",
        "content",
        "vector_score").sort_by("vector_score").dialect(2)

    try:
        results = client.ft("posts").search(
            query, query_params={"vector": query_vector})
    except Exception as e:
        print("Error calling Redis search: ", e)
        return None
    
    if results.total == 0:
        print("No results found for the given query vector.")
        return None
    elif results.total < top_k:
        print(f"Only {results.total} results found for the given query vector.")

    return results

# Connect to the Redis server
conn = redis.Redis(host=redis_host,
                   port=redis_port,
                   password=redis_password,
                   encoding='utf-8',
                   decode_responses=True)

if conn.ping():
    print("Connected to Redis")

# Enter a query
query = input("Enter your query: ")

# Vectorize the query using OpenAI's text-embedding-ada-002 model
print("Vectorizing query...")
embedding = client.embeddings.create(input=query, model="text-embedding-ada-002")
query_vector = embedding.data[0].embedding

# Convert the vector to a numpy array
query_vector = np.array(query_vector).astype(
                        np.float32).tobytes()

# Perform the similarity search
print("Searching for similar posts...")
#results = search_vectors(query_vector, conn)
results = hybrid_search(query_vector, conn)

if results:
    print(f"Found {results.total} results:")
    for i, post in enumerate(results.docs):
        score = 1 - float(post.vector_score)
        print(post.content)
        if DEBUG:
            print(f"\t{i}. {post.title}, {post.publish_date} (Score: {round(score ,3) }) \n\t\t{post.description} \n\t\t{post.url} \n\t\t{post.content}")
else:
    print("No results found")
