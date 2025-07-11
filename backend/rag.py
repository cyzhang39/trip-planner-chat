from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import requests

# dotenv_path = "configs/.env"
load_dotenv()

PROMPT = """
You are a travel assistant.
Use itineraries and information below as reference if they are relevant, to craft a day-by-day itinerary.
Always answer in plain text, no markdown or styling characters.
When you output the itinerary, structure it exactly like this:

#Day 1: <Day 1 activities> | Addresses: <Address 1>; <Address 2>; …  
#Day 2: <Day 2 activities> | Addresses: <Address 1>; <Address 2>; …  
…  
#Day N: <Day N activities> | Addresses: <Address 1>; <Address 2>; …

Be detailed about activities. Use one line per day.
"""

API_KEY=os.getenv("HF_KEY")
BASE_URL=os.getenv("HF_BASE_URL")
RETRIEVE_URL=os.getenv("RETRIEVE_URL")
MODEL="meta-llama/Llama-3.3-70B-Instruct-Turbo"

DEBUG=False

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

def extract_addresses(itinerary_text):
    day_addrs = {}
    pattern = re.compile(r'^#?Day\s+(\d+):.*\|\s*Addresses:\s*(.+)$')
    for line in itinerary_text.splitlines():
        m = pattern.match(line)
        if not m:
            continue
        day = int(m.group(1))
        addrs = [a.strip() for a in m.group(2).split(';') if a.strip()]
        day_addrs[day] = addrs
    return day_addrs

def build_query(req):
    activities = ", ".join(req.activities)
    extras = req.extras or "None"
    info = f"Plan a detailed trip from {req.start_date} to {req.end_date} in {req.region}, for {req.party_size} people, with a budget per person of {req.budget}/day. Interested in {activities}. Extras: {extras}."
    return info

def followup_query(question, history):
    context = " ".join(turn["text"] for turn in history[-5:])
    info = f"{context}\nFollow-up question: {question}"
    return info


def retrieve(query, k=3):
    resp = requests.post(RETRIEVE_URL, json={"query": query, "k": k})
    resp.raise_for_status()
    return resp.json()["documents"]


def generate_itinerary(query, docs):
    if DEBUG:
        return docs[0]["page_content"][:100] if docs else "No documents retrieved."


    messages = [{"role": "system", "content": PROMPT}]
    for d in docs:
        messages.append({"role": "system", "content": d["page_content"]})
    messages.append({"role": "user", "content": query})

    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.1,
        stream=False
    )

    return resp.choices[0].message.content

def followup(question, history, docs):
    if DEBUG:
        return docs[0]["page_content"][:100] if docs else "No documents retrieved."
    messages = [{"role": "system", "content": PROMPT}]
    for d in docs:
        messages.append({"role": "system", "content": d["page_content"]})

    for msg in history:
        role = "user" if msg["from"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["text"]})

    messages.append({"role": "user", "content": question})

    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.1
    )
    return resp.choices[0].message.content    