# websocket/db.py
import sqlite3
from flask import g

DATABASE = 'database.db'


def get_db():
    """
    Opens a new database connection if there is none yet for the current application context.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Allow dictionary-like row access.
    return db


def init_db(app):
    """
    Initialize the SQLite database by creating the 'pump_status' table if it doesn't exist.
    """
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pump_status (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                status TEXT NOT NULL CHECK(status IN ('on', 'off'))
            )
        ''')
        # Ensure there is always one row (id = 1) present.
        cursor.execute("SELECT COUNT(*) as count FROM pump_status")
        row = cursor.fetchone()
        if row['count'] == 0:
            cursor.execute(
                "INSERT INTO pump_status (id, status) VALUES (1, 'off')")
        db.commit()
