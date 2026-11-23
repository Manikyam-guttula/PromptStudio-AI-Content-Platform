
import os
import sqlite3
import webbrowser

from pathlib import Path
from threading import Timer
from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from dotenv import load_dotenv

from services.ai_service import generate_ai_response


# ==================================================
# 1. PROJECT CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "promptstudio-development-secret-key"
)

# VERCEL FIX:
# Vercel deployment files are read-only.
# Use /tmp for SQLite when running on Vercel.
# Local development continues using the existing database.

if os.getenv("VERCEL"):
    DB_PATH = Path("/tmp/promptstudio.db")
else:
    DB_PATH = BASE_DIR / "instance" / "promptstudio.db"
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


# ==================================================
# 2. DATABASE CONNECTION
# ==================================================

def get_db_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


# ==================================================
# 3. DATABASE INITIALIZATION
# ==================================================

def init_db():

    conn = get_db_connection()

    try:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS prompt_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                feature TEXT,
                user_input TEXT,
                ai_response TEXT,
                input_text TEXT,
                output_text TEXT,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        history_columns = [
            row["name"]
            for row in conn.execute(
                "PRAGMA table_info(prompt_history)"
            ).fetchall()
        ]

        required_history_columns = {
            "user_id": "INTEGER",
            "feature": "TEXT",
            "user_input": "TEXT",
            "ai_response": "TEXT",
            "input_text": "TEXT",
            "output_text": "TEXT",
            "result": "TEXT",
            "created_at": "TIMESTAMP"
        }

        for column, datatype in required_history_columns.items():

            if column not in history_columns:
                conn.execute(
                    f'ALTER TABLE prompt_history ADD COLUMN "{column}" {datatype}'
                )

        user_columns = [
            row["name"]
            for row in conn.execute(
                "PRAGMA table_info(users)"
            ).fetchall()
        ]

        if "email" not in user_columns:
            conn.execute(
                "ALTER TABLE users ADD COLUMN email TEXT"
            )

        if "username" not in user_columns:
            conn.execute(
                "ALTER TABLE users ADD COLUMN username TEXT"
            )

        password_columns = [
            "password_hash",
            "hashed_password",
            "password"
        ]

        if not any(col in user_columns for col in password_columns):
            conn.execute(
                "ALTER TABLE users ADD COLUMN password_hash TEXT"
            )

        conn.commit()

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()


init_db()


# ==================================================
# 4. PASSWORD COLUMN DETECTION
# ==================================================

def get_password_column(conn):

    columns = [
        row["name"]
        for row in conn.execute(
            "PRAGMA table_info(users)"
        ).fetchall()
    ]

    for column in [
        "password_hash",
        "hashed_password",
        "password"
    ]:

        if column in columns:
            return column

    conn.execute(
        "ALTER TABLE users ADD COLUMN password_hash TEXT"
    )

    return "password_hash"


# ==================================================
# 5. LOGIN REQUIRED DECORATOR
# ==================================================

def login_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:
            flash("Please login to continue.", "error")
            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return decorated_function


# ==================================================
# 6. AI TOOLS
# ==================================================

TOOLS = {

    "content": {
        "title": "AI Content Generator",
        "description": "Generate high-quality content using AI.",
        "icon": "✍️",
        "prompt": "Generate high-quality content about:"
    },

    "summarizer": {
        "title": "Text Summarizer",
        "description": "Summarize long text into simple and clear points.",
        "icon": "📝",
        "prompt": "Summarize the following text clearly:"
    },

    "sentiment": {
        "title": "Sentiment Analysis",
        "description": "Analyze the sentiment of your text.",
        "icon": "😊",
        "prompt": "Analyze the sentiment of the following text. Identify whether it is positive, negative, or neutral and explain why:"
    },

    "email": {
        "title": "Email Generator",
        "description": "Create professional emails in seconds.",
        "icon": "📧",
        "prompt": "Write a professional email based on these details:"
    },

    "paraphrase": {
        "title": "Paraphrasing Tool",
        "description": "Rewrite text while keeping its original meaning.",
        "icon": "🔄",
        "prompt": "Paraphrase the following text while preserving its original meaning:"
    },

    "grammar": {
        "title": "Grammar Correction",
        "description": "Correct grammar and improve sentence structure.",
        "icon": "✅",
        "prompt": "Correct the grammar and improve the following text:"
    },

    "caption": {
        "title": "Social Media Caption Generator",
        "description": "Generate creative social media captions.",
        "icon": "📱",
        "prompt": "Create an engaging social media caption about:"
    },

    "blog_titles": {
        "title": "Blog Title Generator",
        "description": "Generate attractive and SEO-friendly blog titles.",
        "icon": "💡",
        "prompt": "Generate creative and SEO-friendly blog titles for:"
    }

}


# ==================================================
# 7. SAVE PROMPT HISTORY
# ==================================================

def save_prompt_history(user_id, feature, user_input, ai_response):

    conn = get_db_connection()

    try:

        table_info = conn.execute(
            "PRAGMA table_info(prompt_history)"
        ).fetchall()

        values = {
            "user_id": user_id,
            "feature": feature,
            "user_input": user_input,
            "ai_response": ai_response,
            "input_text": user_input,
            "output_text": ai_response,
            "result": ai_response,
            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        insert_columns = []
        insert_values = []

        for info in table_info:

            column = info["name"]

            if column == "id":
                continue

            if column in values:
                insert_columns.append(f'"{column}"')
                insert_values.append(values[column])

            elif info["notnull"] and info["dflt_value"] is None:
                insert_columns.append(f'"{column}"')
                insert_values.append("")

        placeholders = ", ".join(["?"] * len(insert_values))
        column_names = ", ".join(insert_columns)

        query = f"""
            INSERT INTO prompt_history ({column_names})
            VALUES ({placeholders})
        """

        conn.execute(query, insert_values)
        conn.commit()

    except sqlite3.Error:
        conn.rollback()
        raise

    finally:
        conn.close()


# ==================================================
# 8. HOME ROUTE
# ==================================================

@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


# ==================================================
# 9. REGISTER ROUTE
# ==================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash(
                "Password must contain at least 6 characters.",
                "error"
            )
            return redirect(url_for("register"))

        conn = get_db_connection()

        try:

            existing_user = conn.execute(
                """
                SELECT id FROM users
                WHERE LOWER(username) = LOWER(?)
                   OR LOWER(email) = LOWER(?)
                LIMIT 1
                """,
                (username, email)
            ).fetchone()

            if existing_user:
                flash(
                    "Username or email already registered.",
                    "error"
                )
                return redirect(url_for("register"))

            password_column = get_password_column(conn)

            user_info = conn.execute(
                "PRAGMA table_info(users)"
            ).fetchall()

            values = {
                "username": username,
                "email": email,
                password_column: generate_password_hash(password),
                "created_at": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }

            insert_columns = []
            insert_values = []

            for column_info in user_info:

                column = column_info["name"]

                if column == "id":
                    continue

                if column in values:
                    insert_columns.append(f'"{column}"')
                    insert_values.append(values[column])

                elif (
                    column_info["notnull"]
                    and column_info["dflt_value"] is None
                ):
                    insert_columns.append(f'"{column}"')
                    insert_values.append("")

            placeholders = ", ".join(["?"] * len(insert_values))

            query = f"""
                INSERT INTO users ({", ".join(insert_columns)})
                VALUES ({placeholders})
            """

            conn.execute(query, insert_values)
            conn.commit()

            flash(
                "Account created successfully! Please login.",
                "success"
            )

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            conn.rollback()
            flash(
                "Username or email already exists.",
                "error"
            )
            return redirect(url_for("register"))

        except sqlite3.Error as e:
            conn.rollback()
            flash(f"Registration error: {e}", "error")
            return redirect(url_for("register"))

        finally:
            conn.close()

    return render_template("register.html")


# ==================================================
# 10. LOGIN ROUTE
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash(
                "Please enter your username and password.",
                "error"
            )
            return redirect(url_for("login"))

        conn = get_db_connection()

        try:

            user = conn.execute(
                """
                SELECT * FROM users
                WHERE LOWER(username) = LOWER(?)
                   OR LOWER(email) = LOWER(?)
                LIMIT 1
                """,
                (username, username)
            ).fetchone()

            if not user:
                flash(
                    "Account not found. Please register first.",
                    "error"
                )
                return redirect(url_for("register"))

            user = dict(user)

            password_column = get_password_column(conn)

            stored_password = (
                user.get("password_hash")
                or user.get("hashed_password")
                or user.get("password")
            )

            if not stored_password:
                flash(
                    "Password information is missing for this account.",
                    "error"
                )
                return redirect(url_for("login"))

            password_valid = False

            try:
                password_valid = check_password_hash(
                    stored_password,
                    password
                )
            except (ValueError, TypeError):
                password_valid = False

            if not password_valid and stored_password == password:

                password_valid = True

                conn.execute(
                    f'UPDATE users SET "{password_column}" = ? WHERE id = ?',
                    (
                        generate_password_hash(password),
                        user["id"]
                    )
                )

                conn.commit()

            if not password_valid:
                flash(
                    "Incorrect password. Please try again.",
                    "error"
                )
                return redirect(url_for("login"))

            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            flash("Login successful!", "success")

            return redirect(url_for("dashboard"))

        finally:
            conn.close()

    return render_template("login.html")


# ==================================================
# 11. LOGOUT ROUTE
# ==================================================

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out.", "success")

    return redirect(url_for("login"))


# ==================================================
# 12. DASHBOARD ROUTE
# ==================================================

@app.route("/dashboard")
@login_required
def dashboard():

    conn = get_db_connection()

    try:

        total_prompts = conn.execute(
            """
            SELECT COUNT(*) AS total
            FROM prompt_history
            WHERE user_id = ?
            """,
            (session["user_id"],)
        ).fetchone()["total"]

    finally:
        conn.close()

    return render_template(
        "dashboard.html",
        total_prompts=total_prompts,
        tools=TOOLS
    )


# ==================================================
# 13. HISTORY ROUTE
# ==================================================

@app.route("/history")
@login_required
def history():

    conn = get_db_connection()

    try:

        history_columns = [
            row["name"]
            for row in conn.execute(
                "PRAGMA table_info(prompt_history)"
            ).fetchall()
        ]

        input_column = next(
            (
                col for col in ["user_input", "input_text"]
                if col in history_columns
            ),
            None
        )

        output_column = next(
            (
                col for col in ["ai_response", "output_text", "result"]
                if col in history_columns
            ),
            None
        )

        records = conn.execute(
            """
            SELECT * FROM prompt_history
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (session["user_id"],)
        ).fetchall()

        history_items = []

        for record in records:

            item = dict(record)

            item["feature"] = item.get("feature") or "AI Tool"
            item["user_input"] = (
                item.get(input_column) if input_column else ""
            ) or ""
            item["ai_response"] = (
                item.get(output_column) if output_column else ""
            ) or ""

            history_items.append(item)

    finally:
        conn.close()

    return render_template(
        "history.html",
        history=history_items
    )


# ==================================================
# 14. ANALYTICS ROUTE
# ==================================================

@app.route("/analytics")
@login_required
def analytics():

    conn = get_db_connection()

    try:

        user_id = session["user_id"]

        total_result = conn.execute(
            """
            SELECT COUNT(*) AS total
            FROM prompt_history
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

        total_prompts = total_result["total"] if total_result else 0

        tools_result = conn.execute(
            """
            SELECT COUNT(DISTINCT feature) AS total
            FROM prompt_history
            WHERE user_id = ?
              AND feature IS NOT NULL
              AND TRIM(feature) != ''
            """,
            (user_id,)
        ).fetchone()

        tools_used = tools_result["total"] if tools_result else 0

        usage_rows = conn.execute(
            """
            SELECT feature, COUNT(*) AS count
            FROM prompt_history
            WHERE user_id = ?
              AND feature IS NOT NULL
              AND TRIM(feature) != ''
            GROUP BY feature
            ORDER BY count DESC
            """,
            (user_id,)
        ).fetchall()

        tool_stats = [
            {
                "feature": row["feature"],
                "count": row["count"]
            }
            for row in usage_rows
        ]

        recent_rows = conn.execute(
            """
            SELECT *
            FROM prompt_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 5
            """,
            (user_id,)
        ).fetchall()

        recent_activity = []

        for row in recent_rows:

            item = dict(row)

            item["feature"] = item.get("feature") or "AI Tool"

            item["user_input"] = (
                item.get("user_input")
                or item.get("input_text")
                or "No input available"
            )

            item["created_at"] = (
                item.get("created_at")
                or "Date unavailable"
            )

            recent_activity.append(item)

    finally:
        conn.close()

    return render_template(
        "analytics.html",
        total_prompts=total_prompts,
        tools_used=tools_used,
        tool_stats=tool_stats,
        recent_activity=recent_activity
    )


# ==================================================
# 15. AI TOOL PROCESSING
# ==================================================

def process_tool(tool_key):

    tool = TOOLS.get(tool_key)

    if not tool:
        return "Tool not found", 404

    if request.method == "GET":

        return render_template(
            "tool.html",
            tool=tool,
            tool_key=tool_key
        )

    user_input = request.form.get(
        "user_input",
        ""
    ).strip()

    if not user_input:
        return jsonify({
            "success": False,
            "error": "Please enter some text first."
        }), 400

    prompt = f"""
    {tool["prompt"]}

    {user_input}

    Provide a clear, useful, well-formatted response.
    """

    try:

        ai_response = generate_ai_response(prompt)

        if not ai_response:
            return jsonify({
                "success": False,
                "error": "AI could not generate a response. Please try again."
            }), 500

        save_prompt_history(
            session["user_id"],
            tool["title"],
            user_input,
            ai_response
        )

        return jsonify({
            "success": True,
            "result": ai_response
        })

    except Exception:

        app.logger.exception("AI tool processing failed")

        return jsonify({
            "success": False,
            "error": "AI generation failed. Please check your API configuration and try again."
        }), 500


# ==================================================
# 16. REGISTER ALL AI TOOL ROUTES
# ==================================================

for tool_key in TOOLS:

    app.add_url_rule(
        f"/tools/{tool_key}",
        endpoint=tool_key,
        view_func=login_required(
            lambda key=tool_key: process_tool(key)
        ),
        methods=["GET", "POST"]
    )


# ==================================================
# 17. 404 ERROR PAGE
# ==================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


# ==================================================
# 18. START APPLICATION
# ==================================================

if __name__ == "__main__":

    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5000")

    Timer(1.5, open_browser).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )
