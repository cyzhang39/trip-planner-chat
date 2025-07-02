from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from .rag import generate_itinerary, retrieve, build_query, followup

app = FastAPI()

origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,
    allow_methods=["*"],        
    allow_headers=["*"],        
)

query = ""
docs = None


class TripRequest(BaseModel):
    start_date: str
    end_date: str
    party_size: int
    budget: str
    region: str
    activities: List[str]
    extras: str = ""

class TripResponse(BaseModel):
    itinerary: str

class ChatRequest(BaseModel):
    question: str
    chat_history: List[dict]

class ChatResponse(BaseModel):
    answer: str

@app.post("/api/plan", response_model=TripResponse)
async def plan_trip(req: TripRequest):
    global query
    global docs
    query = build_query(req)
    docs = retrieve(query, 3)
    itinerary_text = generate_itinerary(query, docs)
    return TripResponse(itinerary=itinerary_text)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    answer = followup(req.question, req.chat_history, docs)
    return ChatResponse(answer=answer)