import sqlite3

# =========================
# KONEKSI DATABASE
# =========================
conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =========================
# MEMBUAT TABEL
# =========================
def init_db():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            region TEXT,
            searching INTEGER DEFAULT 0,
            partner INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()

# =========================
# TAMBAH USER
# =========================
def add_user(user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO users(id) VALUES(?)",
        (user_id,)
    )
    conn.commit()

# =========================
# SIMPAN REGION
# =========================
def save_region(user_id, region):
    cursor.execute(
        "UPDATE users SET region=? WHERE id=?",
        (region, user_id)
    )
    conn.commit()

# =========================
# AMBIL REGION
# =========================
def get_region(user_id):
    cursor.execute(
        "SELECT region FROM users WHERE id=?",
        (user_id,)
    )
    data = cursor.fetchone()

    if data:
        return data[0]

    return None

# =========================
# STATUS SEARCH
# =========================
def set_search(user_id, status):
    cursor.execute(
        "UPDATE users SET searching=? WHERE id=?",
        (status, user_id)
    )
    conn.commit()

# =========================
# CARI MATCH BERDASARKAN REGION
# =========================
def find_match(user_id, region):
    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE searching=1
          AND partner=0
          AND id != ?
          AND region=?
        LIMIT 1
        """,
        (user_id, region)
    )

    data = cursor.fetchone()

    if data:
        return data[0]

    return None

# =========================
# SET PARTNER
# =========================
def set_partner(user_id, partner):
    cursor.execute(
        "UPDATE users SET partner=? WHERE id=?",
        (partner, user_id)
    )
    conn.commit()

# =========================
# GET PARTNER
# =========================
def get_partner(user_id):
    cursor.execute(
        "SELECT partner FROM users WHERE id=?",
        (user_id,)
    )

    data = cursor.fetchone()

    if data:
        return data[0]

    return 0

# =========================
# HAPUS PARTNER
# =========================
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

# =========================
# STATISTIK BOT
# =========================
def total_users():
    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    return cursor.fetchone()[0]

def searching_users():
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE searching=1"
    )

    return cursor.fetchone()[0]

def active_chat():
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE partner!=0"
    )

    return cursor.fetchone()[0] // 2
