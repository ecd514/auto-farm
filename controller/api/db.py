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

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                temperature REAL NOT NULL,
                chance_of_rain INTEGER NOT NULL CHECK(chance_of_rain BETWEEN 0 AND 100),
                detailed_forecast TEXT NOT NULL,
                icon_url TEXT NOT NULL,
                generation_time TEXT NOT NULL,
                expiration_time TEXT NOT NULL
            )
        ''')
        cursor.execute("SELECT COUNT(*) as count FROM weather_data")
        row = cursor.fetchone()
        if row['count'] == 0:
            cursor.execute(
                '''INSERT INTO weather_data (
                    id,
                    temperature,
                    chance_of_rain,
                    detailed_forecast,
                    icon_url,
                    generation_time,
                    expiration_time
                ) VALUES (
                1,
                -99,
                0,
                'blank table',
                'http://127.0.0.1:80/',
                '0000-00-00T00:00:00+00:00',
                '9999-12-31T23:59:59+00:00'
                )''')

        db.commit()


def is_database_initialized(table_to_check: str):
    """
    Checks if the SQLite database is initialized by verifying if the weather_data table exists.
    Returns True if initialized, otherwise False.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Check if the table "weather_data" exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(table_to_check))
        table_exists = cursor.fetchone() is not None

        conn.close()
        return table_exists

    except sqlite3.Error as error_database:
        print("Error checking database initialization:", error_database)
        return False
