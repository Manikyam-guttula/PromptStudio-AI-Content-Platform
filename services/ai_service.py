
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

client = Groq(api_key=API_KEY) if API_KEY else None


def generate_ai_response(prompt):

    if not client:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Check your .env file."
        )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are PromptStudio, a helpful AI writing "
                    "and productivity assistant. Give clear, "
                    "accurate and well-formatted answers."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_completion_tokens=1500
    )

    return response.choices[0].message.content.strip()
