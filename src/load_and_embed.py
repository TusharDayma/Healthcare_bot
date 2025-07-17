import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from config import DATA_PATH, CHROMA_PATH, EMBED_MODEL

# Load PDFs
data = []
for file in os.listdir(DATA_PATH):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(DATA_PATH, file))
        data.extend(loader.load())

print(f"✅ Loaded {len(data)} documents")

# Split
splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=500)
chunks = splitter.split_documents(data)
print(f"✅ Split into {len(chunks)} chunks")

# Embed
embedding_model = OllamaEmbeddings(model=EMBED_MODEL)
vectorstore = Chroma.from_documents(chunks, embedding=embedding_model, persist_directory=CHROMA_PATH)

print("✅ Vector store saved")
