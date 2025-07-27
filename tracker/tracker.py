import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

DB_PATH = Path("tracker/job_applications.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            job_title TEXT,
            company TEXT,
            job_url TEXT,
            resume_file TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_application(job_title, company, job_url, resume_file, status):
    timestamp = datetime.now().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO applications (timestamp, job_title, company, job_url, resume_file, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, job_title, company, job_url, resume_file, status))
    conn.commit()
    conn.close()
    print(f" Logged: {job_title} at {company} [{status}]")

# Fetch all logs
def fetch_all_logs():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM applications ORDER BY timestamp DESC", conn)
    conn.close()
    return df
