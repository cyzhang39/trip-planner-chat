from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Any
import torch
from dotenv import load_dotenv
import os
import traceback

from huggingface_hub import InferenceClient
from langchain_community.vectorstores import FAISS

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
# device = "cuda" if torch.cuda.is_available() else "cpu"

client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN,
)

class QwenEmbeddings:
    def __init__(self, client, model):
        self.client = client
        self.model = model

    def embed_documents(self, texts):
        return self.client.feature_extraction(texts, model=self.model)

    def embed_query(self, text):
        return self.embed_documents([text])[0]

    def __call__(self, text):
        return self.embed_query(text)

embedder = QwenEmbeddings(
    client=client,
    model="Qwen/Qwen3-Embedding-8B",
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