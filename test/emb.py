import os
import requests
from dotenv import load_dotenv
from pathlib import Path


# dotenv_path = "configs/.env"
load_dotenv()
API_KEY=os.getenv("HF_KEY")
EMB_URL=os.getenv("HF_EMB_URL")

print(API_KEY)
API_URL = EMB_URL
headers = {
    "Authorization": f"Bearer {API_KEY}",
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output = query({
    "inputs": "Today is a sunny day and I will get some ice cream.",
})

print(output.shape)