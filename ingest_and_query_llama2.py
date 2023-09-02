from langchain.document_loaders import ReadTheDocsLoader,PyPDFLoader
from langchain.embeddings.base import Embeddings
# from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter,CharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from typing import List
import time
import os
import ray
# from embeddings import LocalHuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings,SentenceTransformerEmbeddings
# To download the files locally for processing, here's the command line
# wget -e robots=off --recursive --no-clobber --page-requisites --html-extension \
# --convert-links --restrict-file-names=windows \
# --domains docs.ray.io --no-parent https://docs.ray.io/en/master/

from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA

FAISS_INDEX_PATH="faiss_index"

def ingest_pdf(query):
    loader = PyPDFLoader("docs/2.pdf")
    documents = loader.load()
    # Split document in chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")
    docs = text_splitter.split_documents(documents=documents)
    # Stage one: read all the docs, split them into chunks. 
    st = time.time() 
    print('Loading documents ...')
    # docs = loader.load()
    #Theoretically, we could use Ray to accelerate this, but it's fast enough as is. 
    # chunks = text_splitter.create_documents([doc.page_content for doc in docs], metadatas=[doc.metadata for doc in docs])
    et = time.time() - st
    print(f'Time taken: {et} seconds.') 
    # chunks =['weewewew','ewewe']
    #Stage two: embed the docs. 
    # embeddings = LocalHuggingFaceEmbeddings('multi-qa-mpnet-base-dot-v1')
    embeddings = SentenceTransformerEmbeddings(model_name="/Users/sindhu/prakash/embedding_models/all-MiniLM-L6-v2")
    print(f'Loading chunks into vector store ...') 
    st = time.time()
    # print(docs)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(FAISS_INDEX_PATH)
    et = time.time() - st
    print(f'Time taken: {et} seconds.')

def query_pdf(query):
    # loader = ReadTheDocsLoader("docs.ray.io/en/master/")

    # text_splitter = RecursiveCharacterTextSplitter(
    #     # Set a really small chunk size, just to show.
    #     chunk_size = 300,
    #     chunk_overlap  = 20,
    #     length_function = len,
    # )

    n_gpu_layers = 1  # Metal set to 1 is enough.
    n_batch = 512  # Should be between 1 and n_ctx, consider the amount of RAM of your Apple Silicon Chip.
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    embeddings = SentenceTransformerEmbeddings(model_name="/Users/sindhu/prakash/embedding_models/all-MiniLM-L6-v2")
     # Load from local storage
    persisted_vectorstore = FAISS.load_local("faiss_index", embeddings)

    # Make sure the model path is correct for your system!
    llm_llama2 = LlamaCpp(
        model_path="/Users/sindhu/prakash/LLM-HF-models/llama-2-7b-chat.ggmlv3.q8_0/llama-2-7b-chat.ggmlv3.q8_0.bin",
        # n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        n_ctx=8192,
        f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
        callback_manager=callback_manager,
        verbose=False,
    )
        # Use RetrievalQA chain for orchestration
    qa = RetrievalQA.from_chain_type(llm=llm_llama2, chain_type="stuff", retriever=persisted_vectorstore.as_retriever())
    result = qa.run(query)
    print(result)

def main():
    query = input("Type in your query: \n")
    while query != "exit":
        query_pdf(query)
        query = input("Type in your query: \n")


if __name__ == "__main__":
    main()