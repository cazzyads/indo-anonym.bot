import sqlite3


conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()


def init_db():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY,

        country TEXT,

        searching INTEGER DEFAULT 0,

        partner INTEGER DEFAULT 0

    )
    """)

    conn.commit()



def add_user(user_id):

    cursor.execute(
        "INSERT OR IGNORE INTO users(id) VALUES(?)",
        (user_id,)
    )

    conn.commit()



def save_country(user_id,country):

    cursor.execute(
        """
        UPDATE users
        SET country=?
        WHERE id=?
        """,
        (country,user_id)
    )

    conn.commit()



def set_search(user_id,status):

    cursor.execute(
        """
        UPDATE users
        SET searching=?
        WHERE id=?
        """,
        (status,user_id)
    )

    conn.commit()



def find_match(user_id):

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE searching=1
        AND id != ?
        LIMIT 1
        """,
        (user_id,)
    )

    result = cursor.fetchone()


    if result:
        return result[0]


    return None



def set_partner(user_id,partner):

    cursor.execute(
        """
        UPDATE users
        SET partner=?
        WHERE id=?
        """,
        (partner,user_id)
    )

    conn.commit()



def get_partner(user_id):

    cursor.execute(
        """
        SELECT partner
        FROM users
        WHERE id=?
        """,
        (user_id,)
    )

    result = cursor.fetchone()


    if result:
        return result[0]


    return 0



def remove_partner(user_id):

    cursor.execute(
        """
        UPDATE users
        SET partner=0,
        searching=0
        WHERE id=?
        """,
        (user_id,)
    )

    conn.commit()
