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

FAISS_INDEX_PATH="faiss_index"

# loader = ReadTheDocsLoader("docs.ray.io/en/master/")

# text_splitter = RecursiveCharacterTextSplitter(
#     # Set a really small chunk size, just to show.
#     chunk_size = 300,
#     chunk_overlap  = 20,
#     length_function = len,
# )

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