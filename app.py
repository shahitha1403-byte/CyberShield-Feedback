from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "feedback.db"


def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            category TEXT NOT NULL,
            rating INTEGER NOT NULL,
            message TEXT NOT NULL,
            submitted_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit_feedback():

    name = request.form["name"]
    email = request.form["email"]
    category = request.form["category"]
    rating = request.form["rating"]
    message = request.form["message"]

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        INSERT INTO feedback
        (name, email, category, rating, message, submitted_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        category,
        rating,
        message,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("success"))


@app.route("/success")
def success():
    return """
    <html>
    <head>
        <title>Feedback Submitted</title>
        <style>
            body {
                background: #050b16;
                color: white;
                font-family: Arial;
                text-align: center;
                padding-top: 120px;
            }

            h1 {
                color: #39d9ff;
            }

            a {
                color: #39d9ff;
                text-decoration: none;
            }
        </style>
    </head>

    <body>
        <h1>✅ Feedback Submitted Successfully!</h1>
        <p>Thank you for helping improve cyber security.</p>
        <br>
        <a href="/">Submit Another Feedback</a>
    </body>
    </html>
    """


@app.route("/admin")
def admin():

    conn = sqlite3.connect(DATABASE)

    feedbacks = conn.execute("""
        SELECT id, name, email, category, rating, message, submitted_at
        FROM feedback
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "admin.html",
        feedbacks=feedbacks,
        total=len(feedbacks)
    )


if __name__ == "__main__":
    init_db()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )