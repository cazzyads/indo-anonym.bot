import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()


def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT,
        age TEXT,
        gender TEXT,
        bio TEXT,
        searching INTEGER DEFAULT 0
    )
    """)
    conn.commit()


def add_user(user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO users(id) VALUES(?)",
        (user_id,)
    )
    conn.commit()


def save_profile(user_id,name,age,gender,bio):
    cursor.execute("""
    UPDATE users 
    SET name=?, age=?, gender=?, bio=?
    WHERE id=?
    """,(name,age,gender,bio,user_id))

    conn.commit()


def get_profile(user_id):
    cursor.execute(
        "SELECT * FROM users WHERE id=?",
        (user_id,)
    )

    return cursor.fetchone()


def set_search(user_id,status):
    cursor.execute(
        "UPDATE users SET searching=? WHERE id=?",
        (status,user_id)
    )
    conn.commit()


def find_match(user_id):

    cursor.execute("""
    SELECT id FROM users
    WHERE searching=1
    AND id != ?
    LIMIT 1
    """,(user_id,))

    data=cursor.fetchone()

    return data[0] if data else None
