from database import get_connection

# -------------------------------
# Chat Messages
# -------------------------------

def add_user_message(message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages(role, content)
        VALUES(?, ?)
        """,
        ("user", message)
    )

    conn.commit()
    conn.close()


def add_ai_message(message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages(role, content)
        VALUES(?, ?)
        """,
        ("assistant", message)
    )

    conn.commit()
    conn.close()


def get_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        ORDER BY id
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "role": row["role"],
            "content": row["content"]
        }
        for row in rows
    ]


# -------------------------------
# Context
# -------------------------------

def save_context(context, sources=None):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM context")

    cursor.execute(
        """
        INSERT INTO context(id, content)
        VALUES(1, ?)
        """,
        (context,)
    )

    cursor.execute("DELETE FROM sources")

    if sources:
        for source in sources:
            cursor.execute(
                """
                INSERT INTO sources(filename)
                VALUES(?)
                """,
                (source,)
            )

    conn.commit()
    conn.close()


def get_context():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT content
        FROM context
        WHERE id = 1
        """
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row["content"]

    return ""


def get_sources():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT filename
        FROM sources
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [row["filename"] for row in rows]


# -------------------------------
# Clear Memory
# -------------------------------

def clear_memory():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages")
    cursor.execute("DELETE FROM context")
    cursor.execute("DELETE FROM sources")

    conn.commit()
    conn.close()