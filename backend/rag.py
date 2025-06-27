from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import requests

dotenv_path = Path(__file__).parent.parent / "configs" / ".env"
load_dotenv(dotenv_path=dotenv_path)

PROMPT = """
You are a travel assistant. 
Use itineraries below as reference if they are relevant, and craft a day-by-day itinerary. 
Be concise (within 4000 tokens).
Always answer in plain text, no markdown or styling characters.
When you output the itinerary, structure it _exactly_ like this:
Day 1: <Day 1 activities>
Day 2: <Day 2 activities>
…
Day N: <Day N activities>
Use one line per day, with “Day X:” at the start, and nothing else.
"""


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

def build_query(req) -> str:
    activities = ", ".join(req.activities)
    extras     = req.extras or "None"
    return (
        f"Plan a trip from {req.start_date} to {req.end_date} in {req.region}, "
        f"for {req.party_size} people, with a budget of {req.budget}/day, "
        f"interested in {activities}. Extras: {extras}."
    )

def retrieve(query:str, k: int = 2):
    resp = requests.post(
        os.getenv("RETRIEVE_URL"),
        json={"query": query, "k": k}
    )
    resp.raise_for_status()
    return resp.json()["documents"]


def generate_itinerary(req) -> str:
    query = build_query(req)

    docs = retrieve(query, 2)

    messages = [
        {
            "role": "system",
            "content": PROMPT 
        }
    ]
    for d in docs:
        messages.append({"role": "system", "content": d["page_content"]})
    messages.append({"role": "user", "content": query})

    resp = client.chat.completions.create(
        model="gpt-4.1:free",
        messages=messages,
        temperature=0.3,
        stream=False
    )

    return resp.choices[0].message.content