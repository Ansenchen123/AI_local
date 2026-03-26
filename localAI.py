import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def main() -> None:
    client = OpenAI(
        base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:8000/v1"),
        api_key=os.getenv("OPENAI_API_KEY", "EMPTY"),
    )

    prompt = os.getenv(
        "OPENAI_SAMPLE_PROMPT",
        "Please introduce yourself and describe what this local model is good at.",
    )

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "your-local-model-name"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        stream=True,
    )

    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
