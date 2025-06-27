from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   # ← import added
from pydantic import BaseModel
from typing import List

from .rag import generate_itinerary

app = FastAPI()

# CORS settings
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

@app.post("/api/plan", response_model=TripRequest)
async def plan_trip(req: TripRequest):
    itinerary_text = generate_itinerary(req)
    print(itinerary_text)
    return TripResponse(itinerary=itinerary_text)

# @app.post("/api/embed", response_model=EmbedRequest)