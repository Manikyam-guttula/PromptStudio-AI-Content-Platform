
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env without overwriting Vercel environment variables
load_dotenv(BASE_DIR / ".env", override=False)


def get_ai_client():
    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Check your Vercel Environment Variables."
        )

    return Groq(api_key=api_key)


def generate_ai_response(instructions, prompt, max_tokens=1200):
    client = get_ai_client()

    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": instructions
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_completion_tokens=max_tokens
    )

    result = response.choices[0].message.content

    if not result:
        raise RuntimeError("The AI returned an empty response.")

    return result.strip()


def generate_content(
    prompt,
    tone="Professional",
    content_type="Social Media Post"
):
    instructions = (
        "You are PromptStudio, a helpful professional AI writing assistant. "
        "Create original, clear and useful content. "
        "Follow the requested content type and writing tone."
    )

    user_prompt = (
        f"Content type: {content_type}\n"
        f"Writing tone: {tone}\n"
        f"User request: {prompt}\n\n"
        "Generate the requested content."
    )

    return generate_ai_response(
        instructions,
        user_prompt,
        max_tokens=1500
    )


def summarize_text(text, length="Medium"):
    instructions = (
        "You are a professional text summarization assistant. "
        "Preserve important facts and meaning. "
        "Do not invent details."
    )

    user_prompt = (
        f"Summarize the following text.\n"
        f"Desired length: {length}\n\n"
        f"Text:\n{text}"
    )

    return generate_ai_response(
        instructions,
        user_prompt,
        max_tokens=1000
    )


def analyze_sentiment(text):
    instructions = (
        "You are a sentiment analysis assistant. "
        "Classify the text as Positive, Negative, or Neutral. "
        "Give a short explanation and identify the main emotional tone."
    )

    return generate_ai_response(
        instructions,
        f"Analyze the sentiment of this text:\n\n{text}",
        max_tokens=500
    )
