# needs these packages installed
# conda install chromadb=0.4.15
# pip install chromadb==0.4.15

import os
import warnings
import asyncio
from PyPDF2 import PdfFileReader
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAITextCompletion, OpenAITextEmbedding
from semantic_kernel.connectors.memory.chroma import ChromaMemoryStore
from tqdm import tqdm

warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv('.env')
OPENAI_KEY = os.getenv('OPENAI_API_BOOK_KEY')
DOG_BOOKS = "./data/dog_books"
#DOG_BOOKS = "./data/dog_books_test"
DEBUG = True
VECTOR_DB = "dog_books"
PERSIST_DIR = "./storage"
ALWAYS_CREATE_VECTOR_DB = False

# Load PDFs and extract text
def load_pdfs():
    docs = []
    total_docs = 0
    total_pages = 0
    filenames = [filename for filename in os.listdir(DOG_BOOKS)
                 if filename.endswith('.pdf')]
    with tqdm(total=len(filenames), desc="Processing PDFs") as pbar_outer:
        for filename in filenames:
            pdf_path = os.path.join(DOG_BOOKS, filename)
            with open(pdf_path, 'rb') as file:
                pdf = PdfFileReader(file, strict=False)
                j = 0
                total_docs += 1
                with tqdm(total=len(pdf.pages),
                            desc="Loading Pages") as pbar_inner:
                    for page in pdf.pages:
                        total_pages += 1
                        j += 1
                        docs.append(page.extract_text())
                        #metadata.append({'page':j, 'source':file.name})
                        pbar_inner.update()
                pbar_outer.update()
    print(f"Processed {total_docs} PDFs with {total_pages} pages.")
    #return docs, metadata
    return docs

# Populate the DB with the PDFs
async def populate_db(kernel: sk.Kernel, docs) -> None:
    for i, doc in enumerate(docs):
        if doc:  # Check if doc is not empty
            try:
                await kernel.memory.save_information(VECTOR_DB, id=str(i), text=doc)
            except Exception as e:
                print(f"Failed to save information for doc {i}: {e}")
                continue  # Skip to the next iteration

# Check if user wants to quit
def check_prompt(user_input):
    if user_input.casefold() == 'quit':
        exit()
    return user_input

# Load the vector DB
async def load_vector_db(kernel: sk.Kernel, vector_db_name: str) -> None:
    if not ALWAYS_CREATE_VECTOR_DB:
        collections = await kernel.memory.get_collections()
        if vector_db_name in collections:
            if DEBUG:
                print(f" Vector DB {vector_db_name} exists in the collections. We will reuse this.")
            return
    
    print(f" Vector DB {vector_db_name} does not exist in the collections.")
    print("Reading the pdfs...")
    
    #pdf_docs, pdf_metadata = load_pdfs()
    pdf_docs = load_pdfs()
    print("Total PDFs loaded: ", len(pdf_docs))
    print("Creating embeddings and vector db of the PDFs...")
    # This may take some time as we call OpenAI embedding API for each row
    await populate_db(kernel, pdf_docs)

# Main function 
async def main():
    if DEBUG:
        print("Starting...")
    
    # Setup Semantic Kernel
    kernel = sk.Kernel()
    kernel.add_text_completion_service("dv", OpenAITextCompletion("text-davinci-003", OPENAI_KEY))
    kernel.add_text_embedding_generation_service("ada", OpenAITextEmbedding("text-embedding-ada-002", OPENAI_KEY))

    if DEBUG:
        print("SK kernel loaded...")
    
    # Specify the type of memory to attach to SK. Here we will use Chroma as it is easy to run it locally
    # You can specify location of Chroma DB files. The DB will be stored in "catalog" directory under current dir
    kernel.register_memory_store(memory_store=ChromaMemoryStore(persist_directory=PERSIST_DIR))
    
    await load_vector_db(kernel, VECTOR_DB)
    if DEBUG:
        print("Vector DB loaded...")

    while True:
        prompt = check_prompt(input(
            'Ask a question against the PDF (type "quit" to exit):'))
        if not prompt:
            print("Please enter a valid question.")
            continue
        
        # Now query the memory for most relevant match using search_async specifying relevance score and "limit" of number of closest documents
        result = await kernel.memory.search(collection=VECTOR_DB, limit=3, min_relevance_score=0.7, query=prompt)
        #print("Answer - Results: ", result)
        if result:
            print(result[0].text)
        else:
            print("No matches found.")

        print("-"*80)

if __name__ == "__main__":
    asyncio.run(main())
