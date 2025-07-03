from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import requests

dotenv_path = "configs/.env"
load_dotenv(dotenv_path=dotenv_path)

PROMPT = """
You are a travel assistant. 
Use itineraries below as reference if they are relevant, and craft a day-by-day itinerary. 
Always answer in plain text, no markdown or styling characters.
When you output the itinerary, structure it _exactly_ like this:
Day 1: <Day 1 activities>
Day 2: <Day 2 activities>
…
Day N: <Day N activities>
Be detailed on activities.
Use one line per day, with “Day X:” at the start, and nothing else.
"""

API_KEY=os.getenv("HF_KEY")
BASE_URL=os.getenv("HF_BASE_URL")
MODEL="meta-llama/Llama-3.3-70B-Instruct-Turbo"

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

def build_query(req):
    activities = ", ".join(req.activities)
    extras = req.extras or "None"
    return (
        f"Plan a detailed trip from {req.start_date} to {req.end_date} in {req.region}, "
        f"for {req.party_size} people, with a budget per person of {req.budget}/day. "
        f"Interested in {activities}. Extras: {extras}."
    )

def retrieve(query:str, k: int = 3):
    resp = requests.post(
        os.getenv("RETRIEVE_URL"),
        json={"query": query, "k": k}
    )
    resp.raise_for_status()
    return resp.json()["documents"]


def generate_itinerary(query, docs):
    messages = [{"role": "system", "content": PROMPT}]
    for d in docs:
        messages.append({"role": "system", "content": d["page_content"]})
    messages.append({"role": "user", "content": query})

    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,
        stream=False
    )

    return resp.choices[0].message.content

def followup(question: str, chat_history: list[dict], docs) -> str:
    messages = [
        {"role": "system", "content": PROMPT}
    ]
    for d in docs:
        messages.append({"role": "system", "content": d["page_content"]})

    for msg in chat_history:
        role = "user" if msg["from"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["text"]})

    messages.append({"role": "user", "content": question})

    # call the model
    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3
    )
    return resp.choices[0].message.content    