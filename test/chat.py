from openai import OpenAI
from dotenv import load_dotenv
import os

# dotenv_path = "configs/.env"
load_dotenv()
API_KEY=os.getenv("HF_KEY")
BASE_URL=os.getenv("HF_BASE_URL")

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

completion = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ],
    max_tokens=1000,
)

print(completion.choices[0].message)