
import os
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from services.ai_service import (
    generate_content,
    summarize_text,
    analyze_sentiment
)

# Project directory
BASE_DIR = Path(__file__).resolve().parent

# Do not overwrite environment variables configured in Vercel
load_dotenv(BASE_DIR / ".env", override=False)

# Flask configuration
app = Flask(__name__)
app.secret_key = os.getenv(
    "SECRET_KEY",
    "development-secret-change-me"
)

# Database configuration
if os.getenv("VERCEL"):
    DB_PATH = "/tmp/promptstudio.db"
else:
    DB_DIR = BASE_DIR / "instance"
    DB_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH = str(DB_DIR / "promptstudio.db")


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS prompt_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feature TEXT NOT NULL,
                user_input TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_history(feature, user_input, result):
    created_at = datetime.now(timezone.utc).isoformat()

    with get_db_connection() as connection:
        connection.execute("""
            INSERT INTO prompt_history
            (feature, user_input, result, created_at)
            VALUES (?, ?, ?, ?)
        """, (feature, user_input, result, created_at))


def get_request_data():
    return request.get_json(silent=True) or {}


def error_response(error, status=500):
    app.logger.error("Request failed: %s", error)

    return jsonify({
        "success": False,
        "error": str(error)
    }), status


# Initialize database
initialize_database()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "success": True,
        "status": "running",
        "application": "PromptStudio"
    })


@app.route("/generate", methods=["POST"])
def content_generator():
    try:
        data = get_request_data()

        prompt = str(data.get("prompt", "")).strip()
        tone = str(data.get("tone", "Professional")).strip()
        content_type = str(
            data.get("content_type", "Social Media Post")
        ).strip()

        if not prompt:
            return jsonify({
                "success": False,
                "error": "Please enter your prompt."
            }), 400

        if len(prompt) > 10000:
            return jsonify({
                "success": False,
                "error": "Prompt is too long."
            }), 400

        result = generate_content(
            prompt,
            tone,
            content_type
        )

        save_history("Content Generator", prompt, result)

        return jsonify({
            "success": True,
            "result": result,
            "content": result
        })

    except Exception as error:
        return error_response(error)


@app.route("/summarize", methods=["POST"])
def text_summarizer():
    try:
        data = get_request_data()

        text = str(data.get("text", "")).strip()
        length = str(data.get("length", "Medium")).strip()

        if not text:
            return jsonify({
                "success": False,
                "error": "Please enter text to summarize."
            }), 400

        if len(text) > 20000:
            return jsonify({
                "success": False,
                "error": "Text is too long."
            }), 400

        if length not in ("Short", "Medium", "Long"):
            length = "Medium"

        result = summarize_text(text, length)

        save_history("Text Summarizer", text, result)

        return jsonify({
            "success": True,
            "result": result,
            "summary": result
        })

    except Exception as error:
        return error_response(error)


@app.route("/sentiment", methods=["POST"])
def sentiment_analyzer():
    try:
        data = get_request_data()

        text = str(data.get("text", "")).strip()

        if not text:
            return jsonify({
                "success": False,
                "error": "Please enter text to analyze."
            }), 400

        if len(text) > 10000:
            return jsonify({
                "success": False,
                "error": "Text is too long."
            }), 400

        result = analyze_sentiment(text)

        save_history("Sentiment Analyzer", text, result)

        return jsonify({
            "success": True,
            "result": result,
            "sentiment": result
        })

    except Exception as error:
        return error_response(error)


@app.route("/history", methods=["GET"])
def prompt_history():
    try:
        with get_db_connection() as connection:
            records = connection.execute("""
                SELECT id, feature, user_input, result, created_at
                FROM prompt_history
                ORDER BY id DESC
                LIMIT 100
            """).fetchall()

        return jsonify({
            "success": True,
            "history": [dict(row) for row in records]
        })

    except Exception as error:
        return error_response(error)


@app.route("/analytics", methods=["GET"])
def analytics():
    try:
        with get_db_connection() as connection:
            total = connection.execute("""
                SELECT COUNT(*) AS total
                FROM prompt_history
            """).fetchone()["total"]

            stats = connection.execute("""
                SELECT feature, COUNT(*) AS count
                FROM prompt_history
                GROUP BY feature
                ORDER BY count DESC
            """).fetchall()

        return jsonify({
            "success": True,
            "total_activities": total,
            "feature_stats": [dict(row) for row in stats]
        })

    except Exception as error:
        return error_response(error)


if __name__ == "__main__":
    import threading
    import webbrowser

    url = "http://127.0.0.1:5000"

    threading.Timer(
        1.5,
        lambda: webbrowser.open(url)
    ).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
