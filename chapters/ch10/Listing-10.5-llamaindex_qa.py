# Name: llama-index
# Version: 0.10.9
# Summary: Interface between LLMs and your data
# Home-page: https://llamaindex.ai

#pip install llama-index==0.10.9
# pip install llama-index-readers-file

import os
from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.readers.file import PDFReader

PERSIST_DIR = "./storage/llamaindex"
DOG_BOOKS = "./data/dog_books/"
#DOG_BOOKS = "./data/dog_books_test/" #Used for testing with one file
DEBUG = True

# Load environment variables
load_dotenv('.env')
OPENAI_KEY = os.getenv('OPENAI_API_BOOK_KEY')
Settings.embed_model = OpenAIEmbedding(api_key=OPENAI_KEY)

# Load or create the index
def load_or_create_index():
    # check if storage already exists
    if not os.path.exists(PERSIST_DIR):
        try:
            print("Loading PDFs from ", DOG_BOOKS)
            parser = PDFReader()
            file_extractor = {".pdf": parser}
            
            # load the documents and create the index
            required_exts = [".pdf"]
            documents = SimpleDirectoryReader(DOG_BOOKS, file_extractor=file_extractor, required_exts=required_exts).load_data()
            print("Loaded ", len(documents), "documents.")
            index = VectorStoreIndex.from_documents(documents, show_progress=True)
            
            # store it for later
            index.storage_context.persist(persist_dir=PERSIST_DIR)
            
            print("Index created and stored in", PERSIST_DIR)
        except Exception as e:
            print("Error while creating index:", e)
            exit()
    else:
        print("Loading existing index from", PERSIST_DIR)
        
        try:
            # load the existing index
            storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
            index = load_index_from_storage(storage_context)
        except Exception as e:
            print("Error while loading index:", e)
            exit()
    return index

# Check if user wants to quit
def check_prompt(user_input):
    user_input = user_input.strip().lower()
    if user_input.casefold() == 'exit' or user_input.casefold() == 'quit':
        exit()
    return user_input

# Main loop
def main():
    index = load_or_create_index()
    query_engine = index.as_query_engine()

    while True:
        prompt = check_prompt(input("Ask a question about dogs:"))
        if not prompt:
            print("Please enter a valid question.")
            continue
            
        response = query_engine.query(prompt)
        print(response)
        
if __name__ == "__main__":
    main()