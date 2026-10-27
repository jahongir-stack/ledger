# Ledger — Expense Tracker

A clean Flask web app for logging and visualizing personal expenses.

---

## ✨ Features

- Add, list, and delete expenses
- Automatic category breakdown with visual bars
- Running total of all spending
- JSON summary API endpoint (`/api/summary`)
- SQLite storage — zero external setup.
---

## 🧩 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | Jinja2 templates, HTML, CSS |

---

## 🚀 Getting Started

```bash
git clone https://github.com/jahongir-stack/ledger.git
cd ledger
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

---

## 📡 API

`GET /api/summary` returns:

```json
{
  "total": 342.50,
  "count": 12,
  "by_category": { "Food": 120.0, "Transport": 45.5 }
}
```

---

## 👨‍💻 Author

**Jahongir Ishimov**
