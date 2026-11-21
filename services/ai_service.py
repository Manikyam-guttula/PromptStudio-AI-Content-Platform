import os
import re

def _openai_response(instructions, user_input):
    """Use the OpenAI API when OPENAI_API_KEY is configured."""
    if not os.getenv("OPENAI_API_KEY"):
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            instructions=instructions,
            input=user_input
        )
        return response.output_text
    except Exception as exc:
        raise RuntimeError(f"AI provider error: {exc}") from exc

def generate_text(prompt, content_type="Blog post", tone="Professional"):
    instructions = (
        "You are a helpful content-generation assistant. "
        "Create clear, useful, original content. Follow the requested format and tone. "
        "Do not invent citations or factual sources."
    )
    request = f"Content type: {content_type}\nTone: {tone}\nUser brief: {prompt}"
    result = _openai_response(instructions, request)
    if result:
        return result
    return (
        f"# {content_type}: {prompt[:70].strip()}\n\n"
        f"**Tone:** {tone}\n\n"
        "This is a demonstration response so you can test the website before connecting an AI API. "
        "Add an API key to the `.env` file to generate original AI content.\n\n"
        f"**Your brief:** {prompt}\n\n"
        "## Suggested structure\n"
        "1. Introduction and context\n"
        "2. Main ideas and supporting details\n"
        "3. Practical example or recommendations\n"
        "4. Conclusion and next steps\n"
    )

def summarize_text(text):
    result = _openai_response(
        "Summarize the supplied text accurately. Preserve its key points. Do not add facts.",
        text
    )
    if result:
        return result
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return " ".join(sentences[:3]) + ("\n\n[Demo summary: connect an AI API for an intelligent summary.]" if len(sentences) > 3 else "\n\n[Demo mode]")

def analyze_sentiment(text):
    result = _openai_response(
        "Classify the sentiment as Positive, Negative, or Neutral. Give a short explanation. "
        "Return concise plain text.",
        text
    )
    if result:
        return result
    positive = {"good", "great", "excellent", "happy", "love", "amazing", "success", "useful", "best"}
    negative = {"bad", "poor", "terrible", "hate", "sad", "worst", "problem", "fail", "angry"}
    words = set(re.findall(r"[a-z']+", text.lower()))
    p, n = len(words & positive), len(words & negative)
    label = "Positive" if p > n else "Negative" if n > p else "Neutral"
    return f"{label} (demo analysis)\nPositive keywords: {p} · Negative keywords: {n}\nConnect an AI API or trained NLP model for more reliable contextual analysis."
