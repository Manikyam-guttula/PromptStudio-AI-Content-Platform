
import os
import sqlite3
import webbrowser
import threading

from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from services.ai_service import (
    generate_text,
    summarize_text,
    analyze_sentiment
)

# Load environment variables
load_dotenv()

# Flask configuration
app = Flask(__name__)

# Database configuration
DB_PATH = os.path.join(
    app.root_path,
    "instance",
    "app.db"
)

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


# Database connection
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Initialize database
def init_db():
    with db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool TEXT NOT NULL,
                prompt TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


# Home page
@app.route("/")
def index():
    return render_template("index.html")


# AI Content Generation
@app.route("/api/generate", methods=["POST"])
def api_generate():

    data = request.get_json(silent=True) or {}

    prompt = (data.get("prompt") or "").strip()
    content_type = data.get("content_type", "Blog post")
    tone = data.get("tone", "Professional")

    if not prompt:
        return jsonify(error="Please enter a prompt."), 400

    try:
        result = generate_text(
            prompt,
            content_type,
            tone
        )

        save_result(
            "Content generation",
            prompt,
            result
        )

        return jsonify(
            result=result,
            mode="AI" if os.getenv("OPENAI_API_KEY") else "Demo"
        )

    except Exception as e:
        app.logger.exception("Content generation failed")
        return jsonify(error=str(e)), 500


# Text Summarization
@app.route("/api/summarize", methods=["POST"])
def api_summarize():

    data = request.get_json(silent=True) or {}

    source = (data.get("text") or "").strip()

    if not source:
        return jsonify(error="Please enter text to summarize."), 400

    try:
        result = summarize_text(source)

        save_result(
            "Summarization",
            source[:500],
            result
        )

        return jsonify(result=result)

    except Exception as e:
        app.logger.exception("Summarization failed")
        return jsonify(error=str(e)), 500


# Sentiment Analysis
@app.route("/api/sentiment", methods=["POST"])
def api_sentiment():

    data = request.get_json(silent=True) or {}

    source = (data.get("text") or "").strip()

    if not source:
        return jsonify(error="Please enter text to analyze."), 400

    try:
        result = analyze_sentiment(source)

        save_result(
            "Sentiment analysis",
            source[:500],
            result
        )

        return jsonify(result=result)

    except Exception as e:
        app.logger.exception("Sentiment analysis failed")
        return jsonify(error=str(e)), 500


# Prompt History
@app.route("/api/history")
def api_history():

    with db() as conn:

        rows = conn.execute("""
            SELECT id, tool, prompt, result, created_at
            FROM generations
            ORDER BY id DESC
            LIMIT 30
        """).fetchall()

    return jsonify(
        items=[dict(row) for row in rows]
    )


# Analytics Dashboard
@app.route("/api/analytics")
def api_analytics():

    with db() as conn:

        total = conn.execute(
            "SELECT COUNT(*) FROM generations"
        ).fetchone()[0]

        by_tool = conn.execute("""
            SELECT tool, COUNT(*) AS count
            FROM generations
            GROUP BY tool
            ORDER BY count DESC
        """).fetchall()

    return jsonify(
        total=total,
        by_tool=[dict(row) for row in by_tool]
    )


# Save Results in Database
def save_result(tool, prompt, result):

    with db() as conn:

        conn.execute("""
            INSERT INTO generations
            (tool, prompt, result, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            tool,
            prompt,
            result,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))


# Initialize database
init_db()


# Run Flask and Automatically Open Browser
if __name__ == "__main__":

    url = "http://127.0.0.1:5000"

    def open_browser():
        webbrowser.open_new(url)

    threading.Timer(
        1.5,
        open_browser
    ).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )
