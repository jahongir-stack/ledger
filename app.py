from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = "expenses.db"

CATEGORIES = ["Food", "Transport", "Housing", "Entertainment", "Health", "Shopping", "Other"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    expenses = conn.execute(
        "SELECT * FROM expenses ORDER BY date DESC, id DESC"
    ).fetchall()

    total = sum(e["amount"] for e in expenses)

    by_category = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]

    conn.close()
    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        by_category=by_category,
        categories=CATEGORIES,
        today=datetime.now().strftime("%Y-%m-%d"),
    )


@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form["title"].strip()
    amount = float(request.form["amount"])
    category = request.form["category"]
    date = request.form["date"]

    if title and amount > 0:
        conn = get_db()
        conn.execute(
            "INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
            (title, amount, category, date),
        )
        conn.commit()
        conn.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/api/summary")
def api_summary():
    conn = get_db()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()

    by_category = {}
    for e in expenses:
        by_category[e["category"]] = by_category.get(e["category"], 0) + e["amount"]

    return jsonify({
        "total": sum(e["amount"] for e in expenses),
        "count": len(expenses),
        "by_category": by_category,
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
