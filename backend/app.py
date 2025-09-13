from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from backend.database.db import SessionLocal, get_db
from backend import schemas, auth, rag, sessions
from backend.database import models
from backend.database.db import Base, engine


Base.metadata.create_all(bind=engine)
print("tables created")

app = FastAPI()
load_dotenv()
ORIGIN = os.getenv('REACT_APP_API_ORIGIN')
PORT = os.getenv('APP_PORT')
# print(ORIGIN)
origins = [ORIGIN, "http://localhost:3000", "http://tripplannerusa.com", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(sessions.router)

class TripRequest(BaseModel):
    session_id: int
    start_date: str
    end_date: str
    party_size: str
    budget: str
    region: str
    activities: List[str]
    extras: str = ""

class TripResponse(BaseModel):
    itinerary: str

class ChatRequest(BaseModel):
    session_id: int
    question: str
    chat_history: List[dict]

class ChatResponse(BaseModel):
    answer: str


@app.post("/api/plan", response_model=TripResponse)
def plan_trip(req: TripRequest, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):

    ss = (db.query(models.ChatSession).filter_by(id=req.session_id, owner_id=current_user.id).first())
    if not ss:
        print("Session not found")

    q = rag.build_query(req)
    # msg = models.Message(session_id=req.session_id, from_user="user", text=q)
    # db.add(msg)
    # db.commit()

    docs = rag.retrieve(q, k=3)
    itinerary = rag.generate_itinerary(q, docs)

    # bot = models.Message(session_id=req.session_id, from_user="bot", text=itinerary)
    # db.add(bot)
    # db.commit()

    return TripResponse(itinerary=itinerary)


@app.post("/api/chat", response_model=ChatResponse)
def chat_followup(req: ChatRequest, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):

    ss = (db.query(models.ChatSession).filter_by(id=req.session_id, owner_id=current_user.id).first())
    if not ss:
        print("Session not found")

    # msg = models.Message(session_id=req.session_id, from_user="user", text=req.question)
    # db.add(msg)
    # db.commit()

    q = rag.followup_query(req.question, req.chat_history)
    # msg = models.Message(session_id=req.session_id, from_user="user", text=q)
    # db.add(msg)
    # db.commit()

    docs = rag.retrieve(q, k=3)
    answer = rag.followup(req.question, req.chat_history, docs)

    bot = models.Message(session_id=req.session_id, from_user="bot", text=answer)
    db.add(bot)
    db.commit()

    return ChatResponse(answer=answer)
