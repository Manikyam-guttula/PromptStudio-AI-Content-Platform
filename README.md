# PromptStudio – AI Content Generation Platform

A Flask-based internship capstone prototype with content generation, text summarization, sentiment analysis, history, and analytics.

## Requirements
- Python 3.10+
- pip
- Optional: OpenAI API key for live AI responses

## Setup (Windows)
```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```
Open http://127.0.0.1:5000

Without an API key, the app runs in demo mode. For live generation, add your API key to `.env` and restart Flask. Keep `.env` private and never upload it to GitHub.

## Current prototype scope
- Content generation (live AI when configured; structured demo response otherwise)
- Summarization (live AI when configured; extractive demo fallback)
- Sentiment analysis (live AI when configured; keyword demo fallback)
- SQLite history and basic analytics

The image generation page, authentication, advanced prompt templates, and production deployment are planned next.
