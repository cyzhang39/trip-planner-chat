from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()   

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")

client = OpenAI(api_key=OPENAI_API_KEY, base_url=BASE_URL)

completion = client.chat.completions.create(
    model="gpt-4.1:free",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
)

print(completion.choices[0].message.content)