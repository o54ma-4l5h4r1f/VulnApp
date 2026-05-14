import sqlite3
import subprocess
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# VULN-1: Hardcoded credentials — detect-secrets and Semgrep catch this
DB_PASSWORD = "shopflow_db_pass_2024!"
API_SECRET_KEY = "sk-prod-a1b2c3d4e5f6g7h8i9j0kABCDEF"


def get_db():
    conn = sqlite3.connect("shopflow.db")
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(id INTEGER PRIMARY KEY, username TEXT, email TEXT, role TEXT)"
    )
    conn.execute(
        "INSERT OR IGNORE INTO users VALUES "
        "(1,'alice','alice@shopflow.com','employee'),"
        "(2,'bob','bob@shopflow.com','employee'),"
        "(3,'carol','carol@shopflow.com','supervisor')"
    )
    conn.commit()
    return conn


@app.route("/api/user")
def get_user():
    # VULN-2: SQL injection — user input concatenated directly into query string
    user_id = request.args.get("id", "1")
    conn = get_db()
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor = conn.execute(query)
    return jsonify(cursor.fetchall())


@app.route("/api/ping")
def ping():
    # VULN-3: OS command injection — shell=True with unsanitized user input
    host = request.args.get("host", "localhost")
    result = subprocess.run(
        f"ping -c 1 {host}", shell=True, capture_output=True, text=True
    )
    return jsonify({"output": result.stdout})


@app.route("/api/debug")
def debug():
    # VULN-4: Information disclosure — exposes all environment variables
    return jsonify(dict(os.environ))


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})


if __name__ == "__main__":
    # VULN-5: debug=True in production enables the interactive Werkzeug debugger
    app.run(debug=True, host="0.0.0.0", port=5000)
STRIPE_SECRET_KEY = "sk_live_newleakedkey12345abcdef"
