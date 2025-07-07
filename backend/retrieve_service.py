from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Any

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedder = HuggingFaceEmbeddings(
    model_name="Qwen/Qwen3-Embedding-0.6B",
    model_kwargs={"device": "cuda"} 
)
vector_store = FAISS.load_local("data/index", embedder, allow_dangerous_deserialization=True)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

class RetrieveRequest(BaseModel):
    query: str
    k: int = 3

class Doc(BaseModel):
    page_content: str
    metadata: Any

class RetrieveResponse(BaseModel):
    documents: List[Doc]

app = FastAPI()

@app.post("/retrieve", response_model=RetrieveResponse)
async def retrieve(req: RetrieveRequest):
    docs = retriever.get_relevant_documents(req.query)
    return RetrieveResponse(documents=[Doc(page_content=d.page_content, metadata=d.metadata) for d in docs])
