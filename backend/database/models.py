from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.schema import Identity
from sqlalchemy.orm import relationship

from backend.database.db import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    sessions = relationship("ChatSession", back_populates="owner", cascade="all, delete-orphan")


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    title = Column(String(100), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan", order_by="Message.id")

class Message(Base):
    __tablename__ = "messages"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    from_user = Column(String(10), nullable=False)
    text = Column(Text, nullable=False)
    session = relationship("ChatSession", back_populates="messages")