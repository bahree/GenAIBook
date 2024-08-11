import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAI, OpenAIEmbeddings
from PyPDF2 import PdfReader

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI
def initialize_openai(api_choice):
    if api_choice == 'OpenAI':
        return OpenAI(api_key=openai_api_key)
    elif api_choice == 'AzureOpenAI':
        return OpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY"))

def get_model_name(api_choice):
    if api_choice == 'OpenAI':
        return os.getenv("OPENAI_MODEL_NAME")
    elif api_choice == 'AzureOpenAI':
        return os.getenv("AZURE_OPENAI_MODEL_NAME")

def sidebar_settings():
    st.sidebar.header("Settings")
    api_choice = st.sidebar.selectbox("Choose API", ["OpenAI", "AzureOpenAI"])
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.sidebar.slider("Max Tokens", 10, 32000, 800)
    
    st.session_state.api_choice = api_choice
    st.session_state.temperature = temperature
    st.session_state.max_tokens = max_tokens

def load_pdfs(uploaded_file):
    docs = []
    temp_dir = "temp"
    
    # Ensure the temp directory exists
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    pdf_path = os.path.join(temp_dir, uploaded_file.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    with open(pdf_path, 'rb') as file:
        pdf = PdfReader(file)
        for i, page in enumerate(pdf.pages):
            docs.append(Document(page_content=page.extract_text(), metadata={'page': i+1, 'source': file.name}))
    return docs

def create_index(docs):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=2048,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, disallowed_special=())
    vectordb = FAISS.from_documents(chunks, embeddings)
    return vectordb

def main():
    st.title("Chat with Your Data 📅")
    
    sidebar_settings()
    
    client = initialize_openai(st.session_state.api_choice)
    model_name = get_model_name(st.session_state.api_choice)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "system", "content": "You are an AI assistant that helps people find information."}]
    
    st.sidebar.header("PDF Upload and RAG")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf", key="file_uploader")
    
    if uploaded_file is not None and "documents" not in st.session_state:
        with st.spinner("Processing PDF..."):
            docs = load_pdfs(uploaded_file)
            st.session_state.documents = docs
            vectordb = create_index(docs)
            st.session_state.vectordb = vectordb
        st.sidebar.success("File processed and index created successfully!")
    
    if "documents" in st.session_state:
        docs = st.session_state.documents
        vectordb = st.session_state.vectordb
        with st.sidebar.expander("PDF Content", expanded=False):
            st.text_area("PDF Content", value="\n".join([doc.page_content for doc in docs]), height=300, disabled=True)
        pdf_query = st.chat_input("Ask something about the PDF: ")
        
        if pdf_query:
            st.session_state.chat_history.append({"role": "user", "content": pdf_query})
            
            similar_docs = vectordb.similarity_search(pdf_query, k=5, fetch_k=10)
            chain = load_qa_chain(client, chain_type='stuff')
            response = chain.invoke({'input_documents': similar_docs, 'question': pdf_query}, return_only_outputs=True)
            
            st.session_state.chat_history.append({"role": "assistant", "content": response['output_text']})
            
            for message in st.session_state.chat_history:
                if message["role"] != "system":
                    st.chat_message(message['role']).write(message['content'])
                    
    if st.sidebar.button("Clear All"):
        for key in ["documents", "vectordb", "chat_history", "file_uploader"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.file_uploader = None

if __name__ == "__main__":
    main()
