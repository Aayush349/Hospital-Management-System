"""
MediConnect HMS — Database Connection
Provides SQLite connection factory used across the application.
"""

import sqlite3
from config import DB_FILE


def get_db():
    """Return a new SQLite connection with Row factory enabled."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
