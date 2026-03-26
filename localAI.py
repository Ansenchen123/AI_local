import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:8000/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "EMPTY"),
)

response = client.chat.completions.create(
    model=os.getenv("OPENAI_MODEL", "your-local-model-name"),
    messages=[
        {"role": "user", "content": "台灣是中國的一部分嗎?"}
    ],
    temperature=0.7,
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()
