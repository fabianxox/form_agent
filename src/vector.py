import os
import sys
import signal
import atexit
import shutil
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

VECTOR_DIR = 'vectorstore'
VECTOR_DB = os.path.join(VECTOR_DIR, 'db_faiss')

def cleanup_embeddings():
    if os.path.exists(VECTOR_DIR):
        shutil.rmtree(VECTOR_DIR)
        print("Old embeddings deleted.")

def handle_signal(signum, frame):
    print(f"\nSignal {signum} received! Cleaning up embeddings...")
    cleanup_embeddings()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)
atexit.register(cleanup_embeddings)

def convert_to_vector(all_content):
    if not os.path.exists(VECTOR_DIR):
        os.makedirs(VECTOR_DIR)
        print(f"Folder '{VECTOR_DIR}' created.")

    if os.path.exists(VECTOR_DB):
        print("Existing vectorstore found. Loading...")
        vector_store = FAISS.load_local(
            VECTOR_DB,
            HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            ),
            allow_dangerous_deserialization=True 
        )
    else:
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " "],
            chunk_size=3000,
            chunk_overlap=50
        )

        all_chunks = []
        for doc in all_content:
            chunks = splitter.split_text(doc.page_content)
            all_chunks.extend(chunks)

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )

        vector_store = FAISS.from_texts(all_chunks, embeddings)

        vector_store.save_local(VECTOR_DB)
        print("Vector store created and saved successfully.")

    return vector_store



def find_relevant_chunk(query, vector_store):
    top_k = 100
    relevant_chunks = vector_store.similarity_search(query, k=top_k)
    #print(relevant_chunks)
    return relevant_chunks