from langchain_community.vectorstores.faiss import FAISS

vector_store = FAISS.from_documents(
    documents,
    embedding=embedder,
)