# db.py
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "health_metrics.db"


def get_connection():
    """Return a SQLite connection to the local database."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create the daily_metrics table if it doesn't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_date TEXT UNIQUE NOT NULL,
                sleep_hours REAL,
                steps INTEGER,
                mood INTEGER,
                notes TEXT
            )
        """)
        conn.commit()


def save_daily_metric(log_date, sleep_hours, steps, mood, notes):
    """Insert a new metric row, or update if the date already exists.
    Returns True on success, False on failure."""
    try:
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO daily_metrics (log_date, sleep_hours, steps, mood, notes)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(log_date) DO UPDATE SET
                    sleep_hours = excluded.sleep_hours,
                    steps       = excluded.steps,
                    mood        = excluded.mood,
                    notes       = excluded.notes
            """, (log_date, sleep_hours, steps, mood, notes))
            conn.commit()
        return True
    except Exception as e:
        print(f"[db.save_daily_metric] Error: {e}")
        return False


def fetch_all_metrics():
    """Return all metrics as a DataFrame, newest first.
    Returns an empty DataFrame if the table has no rows."""
    with get_connection() as conn:
        df = pd.read_sql_query(
            "SELECT log_date, sleep_hours, steps, mood, notes "
            "FROM daily_metrics ORDER BY log_date DESC",
            conn
        )
    return df


def delete_metric_by_date(log_date):
    """Delete the row matching the given log_date (YYYY-MM-DD)."""
    with get_connection() as conn:
        conn.execute("DELETE FROM daily_metrics WHERE log_date = ?", (log_date,))
        conn.commit()