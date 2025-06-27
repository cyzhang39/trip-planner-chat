from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import requests

dotenv_path = Path(__file__).parent.parent / "configs" / ".env"
load_dotenv(dotenv_path=dotenv_path)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

def build_query(req) -> str:
    """Turn the TripRequest model into a single prompt string."""
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
    """
    Full RAG flow:
      1) Build the natural‐language query
      2) Retrieve top-k docs
      3) Assemble system+context messages
      4) Call the OpenAI chat API
      5) Return the assistant’s reply
    """
    query = build_query(req)

    docs = retrieve(query, 2)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful travel assistant. "
                       "Use the facts below to craft a day-by-day itinerary."
        }
    ]
    for d in docs:
        messages.append({"role": "system", "content": d["page_content"]})
    messages.append({"role": "user", "content": query})

    resp = client.chat.completions.create(
        model="gpt-4.1:free",  # swap to your fine-tuned model when ready
        messages=messages,
        temperature=0.3,
        stream=False
    )

    return resp.choices[0].message.content