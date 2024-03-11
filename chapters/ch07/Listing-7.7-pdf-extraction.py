# pip install pypdf2

# Few things to note:
# The accuracy of text extraction depends on the PDF. Not all PDFs encode text in a manner that is easily extractable.
# Consider using the pdfminer library for more complex PDFs or if PyPDF2 doesn't provide satisfactory results.
# The chunking strategy used here is based on character count, but depending on your application, you might want to adopt a more sophisticated strategy that considers tokens, words, or semantic meaning.

import os
import PyPDF2
from openai import OpenAI
from tqdm import tqdm # for progress bars
import tiktoken as tk
import spacy

client = OpenAI(api_key=os.getenv("OPENAI_API_BOOK_KEY"))

# function that extracts text from a PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        print("Number of PDF pages:", len(reader.pages))
        text = ""
        for  page in reader.pages:
            page_text = page.extract_text()
            text += page_text
            #print(page_text)
    return text

# function that splits the text into chunks based on sentences
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
    response = client.embeddings.create(
        model="ada-embedding",
        input=text)
    
    return response.data[0].embedding

# Process the chunks
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

if __name__ == "__main__":
    PDF_PATH = "./data/women_fifa_worldcup_2023.pdf"
    extracted_text = extract_text_from_pdf(PDF_PATH)

    # Assuming a chunk size of 2000 characters for demonstration purposes.
    #chunks = paragraph_split(extracted_text, 2000)
    chunks = split_sentences_by_spacy(extracted_text, 2000)
    
    for index, chunk in enumerate(chunks):
        print(f"--- Chunk {index + 1} ---")
        print(chunk)
        print("---------------\n")
