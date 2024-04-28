import redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.field import TagField

# Redis connection details
# redis_host = os.getenv('REDIS_HOST')
# redis_port = os.getenv('REDIS_PORT')
# redis_password = os.getenv('REDIS_PASSWORD')

redis_host = "localhost"
redis_port = "6379"
redis_password = ""
 
# Connect to the Redis server
conn = redis.Redis(host=redis_host, 
                   port=redis_port,
                   password=redis_password, 
                   encoding='utf-8', 
                   decode_responses=True)

# Define the schema for the index
SCHEMA = [
    TagField("url"),
    TextField("title"), 
    TextField("description"),
    TextField("publish_date"),
    TextField("content"),
    VectorField("embedding", "HNSW", {
        "TYPE": "FLOAT32",
        "DIM": 1536, 
        "DISTANCE_METRIC": "COSINE"}
        ),
]

# Create an index
def create_index(conn, schema, index_name="posts"):
    try:
        conn.ft(index_name).create_index(
            fields=schema,
            definition=IndexDefinition(prefix=["post:"], index_type=IndexType.HASH))
    except Exception as e:
        print("Index already exists")

# Delete an index
def delete_index(conn, index_name="posts"):
    try:
        conn.execute_command('FT.DROPINDEX', index_name)
    except Exception as e:
        print("Failed to delete index: ", e)

# Delete all keys from an index
def delete_all_keys_from_index(conn, index_name="posts"):
    try:
        # 1. Retrieve all document IDs from the index.
        # Note: This assumes the total number of documents isn't extraordinarily large.
        # If it is, you might want to paginate the query.
        result = conn.execute_command('FT.SEARCH', index_name, '*', 'NOCONTENT')

        # 2. Parse the result to get document IDs. Skip the first element which is the total count.
        doc_ids = result[1::2]  # Taking every second element starting from the first.

        # 3. Delete each document key.
        for doc_id in doc_ids:
            conn.delete(doc_id)
            
    except Exception as e:
        print("Failed to delete keys: ", e)

# View index details
def view_index(conn, index_name="posts"):
    try:
        info = conn.execute_command('FT.INFO', index_name)
        for i in range(0, len(info), 2):
            print(f"{info[i]}: {info[i+1]}")
    except Exception as e:
        print("Failed to retrieve index details: ", e)

# Main function
def main():
    while True:
        print("1. View index details 🤘")
        print("2. Create index 😁")
        print("3. Delete index 😭")
        print("4. Exit 🚪")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Call the function to view index
            view_index(conn)
            pass
        elif choice == '2':
            # Call the function to create index
            create_index(conn, SCHEMA)
        elif choice == '3':
            # Call the function to delete index
            delete_all_keys_from_index(conn)
            delete_index(conn)
        elif choice == '4':
            break
        else:
            print("Invalid choice. 🙃 Please enter a valid option.")

if __name__ == "__main__":
    main()