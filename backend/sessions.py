from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.params import Body
from sqlalchemy.orm import Session
from typing import List

from backend.database import models
from backend.database.db import SessionLocal, get_db
from backend import schemas, auth
from backend.schemas import MessageIn, MessageOut

router = APIRouter()

@router.post("/api/sessions", response_model=schemas.SessionOut)
def create_session(db: Session = Depends(get_db), curr: models.User = Depends(auth.get_current_user)):
    ss = models.ChatSession(title="New Chat", owner_id=curr.id)
    db.add(ss)
    db.commit()
    db.refresh(ss)

    greeting = "Hi! I am your trip planner assistant. \nBefore generating your itinerary, please answer a few questions.\nFirst, when do you plan to start this trip (YYYY-MM-DD)?"
    initial = models.Message(
        session_id=ss.id,
        from_user="bot",
        text=greeting
    )
    db.add(initial)
    db.commit()
    db.refresh(ss)
    return ss

@router.get("/api/sessions", response_model=List[schemas.SessionOut])
def list_sessions(db: Session = Depends(get_db), curr: models.User = Depends(auth.get_current_user)):
    return db.query(models.ChatSession).filter(models.ChatSession.owner_id == curr.id).all()

@router.get("/api/sessions/{session_id}", response_model=schemas.SessionOut)
def get_session(session_id: int, db: Session = Depends(get_db), curr: models.User = Depends(auth.get_current_user)):
    ss = db.query(models.ChatSession).filter(models.ChatSession.id == session_id, models.ChatSession.owner_id == curr.id).first()
    
    if not ss:
        raise HTTPException(status_code=404, detail="Session not found")
    return ss

@router.delete("/api/sessions/{session_id}", status_code=204)
def delete_session(session_id: int, db: Session = Depends(get_db), curr: models.User = Depends(auth.get_current_user)):
    ss = db.query(models.ChatSession).filter_by(id=session_id, owner_id=curr.id).first()
    
    if not ss:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(ss)
    db.commit()

@router.post("/api/sessions/{session_id}/messages", response_model=MessageOut, status_code=201)
def add_message(session_id: int = Path(...), msg_in: MessageIn = Body(...), db: Session = Depends(get_db), curr: models.User = Depends(auth.get_current_user)):
    ss = db.query(models.ChatSession).filter_by(id=session_id, owner_id=curr.id).first()
    
    if not ss:
        raise HTTPException(status_code=404, detail="Session not found")

    msg = models.Message(
        session_id=session_id,
        from_user=msg_in.from_user,
        text=msg_in.text
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
