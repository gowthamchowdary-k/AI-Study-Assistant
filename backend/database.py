import sqlite3
import os
import shutil

# Path to the SQLite database file.
# On Vercel, the directory is read-only. We must write to /tmp.
if os.environ.get("VERCEL"):
    DB_PATH = "/tmp/study_assistant.db"
    bundled_db = os.path.join(os.path.dirname(__file__), "study_assistant.db")
    # Copy the bundled database containing our tables if not already in /tmp
    if os.path.exists(bundled_db) and not os.path.exists(DB_PATH):
        try:
            shutil.copy2(bundled_db, DB_PATH)
            os.chmod(DB_PATH, 0o666)
            print(f"Vercel DB setup: Copied database to {DB_PATH}")
        except Exception as e:
            print(f"Vercel DB setup warning: Failed to copy bundled DB ({e}). A new one will be created.")
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "study_assistant.db")


def get_connection():
    """
    Returns a SQLite connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """
    Creates all required tables if they do not exist.
    Handles migration by dropping old tables if they lack the user_id column.
    """

    conn = get_connection()
    cursor = conn.cursor()

    # Check if messages table exists and has user_id
    recreate = False
    try:
        cursor.execute("SELECT id FROM messages LIMIT 1")
        # messages table exists, check if user_id exists in it
        try:
            cursor.execute("SELECT user_id FROM messages LIMIT 1")
        except sqlite3.OperationalError:
            print("Migration required: user_id missing in messages table. Dropping old tables...")
            recreate = True
    except sqlite3.OperationalError:
        # Table doesn't exist, which is fine
        pass

    if recreate:
        cursor.execute("DROP TABLE IF EXISTS messages")
        cursor.execute("DROP TABLE IF EXISTS context")
        cursor.execute("DROP TABLE IF EXISTS sources")

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Chat messages
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Last retrieved document context
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS context (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            content TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # PDF source names used in the last response
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Documents tracking table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            status TEXT NOT NULL,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(user_id, filename)
        )
    """)

    conn.commit()
    conn.close()


# Create tables automatically when imported
initialize_database()


def add_document_record(user_id, filename, original_filename, status):
    """
    Creates a new document tracking record in the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO documents (user_id, filename, original_filename, status, error_message) VALUES (?, ?, ?, ?, NULL)",
            (user_id, filename, original_filename, status)
        )
        conn.commit()
    finally:
        conn.close()


def update_document_status(user_id, filename, status, error_message=None):
    """
    Updates the status of a document tracking record.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE documents SET status = ?, error_message = ? WHERE user_id = ? AND filename = ?",
            (status, error_message, user_id, filename)
        )
        conn.commit()
    finally:
        conn.close()


def get_user_documents(user_id):
    """
    Retrieves all document records for a given user from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT filename, original_filename, status, error_message, created_at FROM documents WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def delete_document_record(user_id, filename):
    """
    Removes a document record from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM documents WHERE user_id = ? AND filename = ?",
            (user_id, filename)
        )
        conn.commit()
    finally:
        conn.close()