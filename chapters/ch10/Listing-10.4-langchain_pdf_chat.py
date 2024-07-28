# Needs the following installed:
# langchain                                  0.1.6
# langchain-community                        0.0.19
# langchain-core                             0.1.23
# langchain-openai                           0.0.6
# opentelemetry-instrumentation-langchain    0.14.3

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAI, OpenAIEmbeddings
from tqdm import tqdm
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv('.env')
OPENAI_KEY = os.getenv('OPENAI_API_BOOK_KEY')
DOG_BOOKS = "./data/dog_books"
DEBUG = False

# Create the index
def create_index():
    try:
        # load the documents and create the index
        docs = load_pdfs()
        if not docs:
            print('No PDFs found.')
            return None
        
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=2048,
            chunk_overlap=200,
            length_function=len
        )
        
        # Convert the chunks of text into embeddings
        print("Chunking and creating embeddings...")
        chunks = text_splitter.split_documents(docs)
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
        vectordb = FAISS.from_documents(chunks, embeddings)
    except Exception as e:
        print("Error while creating index:", e)
        exit()
    return vectordb

# Load the PDFs
def load_pdfs() -> list[Document]:
    docs = []
    total_docs = 0
    total_pages = 0
    filenames = [filename for filename in os.listdir(DOG_BOOKS)
                 if filename.endswith('.pdf')]
    with tqdm(total=len(filenames), desc="Processing PDFs") as pbar_outer:
        for filename in filenames:
            pdf_path = os.path.join(DOG_BOOKS, filename)
            with open(pdf_path, 'rb') as file:
                pdf = PdfReader(file, strict=False)
                j = 0
                total_docs += 1
                with tqdm(total=len(pdf.pages),
                            desc="Loading Pages") as pbar_inner:
                    for page in pdf.pages:
                        total_pages += 1
                        j += 1
                        docs.append(Document(
                            page_content=page.extract_text(),
                            metadata={'page':j, 'source':file.name}
                        ))
                        pbar_inner.update()
                pbar_outer.update()
    print(f"Processed {total_docs} PDFs with {total_pages} pages.")
    return docs

# Check if user wants to quit
def check_prompt(user_input):
    if user_input.casefold() == 'quit':
        exit()
    return user_input

# Main function
def main():
    vectordb = create_index()
    
    if vectordb is None:
        print("No index to query.")
        exit()
        
    llm = OpenAI(openai_api_key=OPENAI_KEY)
    chain = load_qa_chain(llm, chain_type='stuff')

    while True:
        prompt = check_prompt(input(
            'Ask a question against the PDF (type "quit" to exit):'))
        if not prompt:
            print("Please enter a valid question.")
            continue

        docs = vectordb.similarity_search(prompt, k=3, fetch_k=10)
        response = chain.invoke({'input_documents': docs,
                                 'question': prompt},
                                return_only_outputs=True)
        print(f"Answer:\n {response['output_text']}")
        print("-"*80)

if __name__ == "__main__":
    main()