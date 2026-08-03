from database import get_connection

# -------------------------------
# Chat Messages
# -------------------------------

def add_user_message(message, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages(user_id, role, content)
        VALUES(?, ?, ?)
        """,
        (user_id, "user", message)
    )

    conn.commit()
    conn.close()


def add_ai_message(message, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages(user_id, role, content)
        VALUES(?, ?, ?)
        """,
        (user_id, "assistant", message)
    )

    conn.commit()
    conn.close()


def get_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE user_id = ?
        ORDER BY id
        """,
        (user_id,)
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

def save_context(context, user_id, sources=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM context WHERE user_id = ?", (user_id,))

    cursor.execute(
        """
        INSERT INTO context(user_id, content)
        VALUES(?, ?)
        """,
        (user_id, context)
    )

    cursor.execute("DELETE FROM sources WHERE user_id = ?", (user_id,))

    if sources:
        for source in sources:
            cursor.execute(
                """
                INSERT INTO sources(user_id, filename)
                VALUES(?, ?)
                """,
                (user_id, source)
            )

    conn.commit()
    conn.close()


def get_context(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT content
        FROM context
        WHERE user_id = ?
        """,
        (user_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row["content"]

    return ""


def get_sources(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT filename
        FROM sources
        WHERE user_id = ?
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [row["filename"] for row in rows]


# -------------------------------
# Clear Memory
# -------------------------------

def clear_memory(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM context WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM sources WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()