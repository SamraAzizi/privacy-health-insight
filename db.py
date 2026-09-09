import sqlite3
import pandas as pd
from typing import Optional, List, Dict, Any

DB_NAME = "health_data.db"

def get_connection():
    """Establishes and returns a database connection."""
    conn = sqlite3.connect(DB_NAME)
    # Enable row factory so query results can be accessed like dictionaries
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the health_metrics table if it doesn't already exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_date TEXT UNIQUE NOT NULL,
                sleep_hours REAL NOT NULL,
                steps INTEGER NOT NULL,
                mood INTEGER NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_daily_metric(log_date: str, sleep_hours: float, steps: int, mood: int, notes: Optional[str] = ""):
    """
    Inserts a new daily health record or updates an existing record for the given date.
    Uses parameterized placeholders (?) for security against SQL injection.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO health_metrics (log_date, sleep_hours, steps, mood, notes)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(log_date) DO UPDATE SET
                sleep_hours = excluded.sleep_hours,
                steps = excluded.steps,
                mood = excluded.mood,
                notes = excluded.notes,
                created_at = CURRENT_TIMESTAMP
        """, (log_date, sleep_hours, steps, mood, notes))
        conn.commit()

def fetch_all_metrics() -> pd.DataFrame:
    """Retrieves all health logs sorted by date and returns them as a Pandas DataFrame."""
    with get_connection() as conn:
        query = "SELECT log_date, sleep_hours, steps, mood, notes FROM health_metrics ORDER BY log_date ASC"
        df = pd.read_sql_query(query, conn)
        return df

def delete_metric_by_date(log_date: str):
    """Deletes a specific log by date."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM health_metrics WHERE log_date = ?", (log_date,))
        conn.commit()