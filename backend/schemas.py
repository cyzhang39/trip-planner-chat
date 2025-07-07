from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    
class MessageIn(BaseModel):
    from_user: str
    text: str

class MessageOut(BaseModel):
    id: int
    from_user: str
    text: str

    class Config:
        orm_mode = True

class SessionOut(BaseModel):
    id: int
    title: str
    messages: list[MessageOut]

    class Config:
        orm_mode = True
